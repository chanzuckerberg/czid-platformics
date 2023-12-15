"""
GraphQL types, queries, and mutations for files.
"""

import json
import typing
import database.models as db
import strawberry
import tempfile
import uuid
import uuid6
from fastapi import Depends
from typing_extensions import TypedDict
from mypy_boto3_s3.client import S3Client
from mypy_boto3_sts.client import STSClient
from platformics.api.core.deps import get_s3_client
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.api.core.gql_to_sql import EnumComparators, IntComparators, StrComparators, UUIDComparators
from strawberry.scalars import JSON
from strawberry.types import Info
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from support.format_handlers import get_validator
from support.enums import FileStatus
from api.core.helpers import get_db_rows
from api.types.entities import Entity
from platformics.settings import APISettings
from platformics.security.authorization import CerbosAction, get_resource_query
from platformics.api.core.deps import (
    get_cerbos_client,
    get_db_session,
    require_auth_principal,
    get_settings,
    get_sts_client,
)

FILE_CONCATENATION_MAX = 100
FILE_CONCATENATION_MAX_SIZE = 1e6
FILE_CONCATENATION_PREFIX = "tmp/concatenated-files"

# ------------------------------------------------------------------------------
# Utility types/inputs
# ------------------------------------------------------------------------------


@strawberry.type
class SignedURL:
    """
    Signed URLs for downloading a file from S3.
    """

    url: str
    protocol: str
    method: str
    expiration: int
    fields: typing.Optional[JSON] = None  # type: ignore


@strawberry.type
class MultipartUploadCredentials:
    """
    STS token for uploading a file to S3.
    """

    protocol: str
    namespace: str
    path: str
    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: str


# Define graphQL input types so we can pass a "file" JSON to mutations.
# Keep them separate so we can control which fields are required.
@strawberry.input()
class FileUpload:
    """
    GraphQL input type for uploading a file.
    """

    name: str
    file_format: str
    compression_type: typing.Optional[str] = None


@strawberry.input()
class FileCreate:
    """
    GraphQL input type for creating a File object based on an existing S3 file (no upload).
    """

    name: str
    file_format: str
    compression_type: typing.Optional[str] = None
    protocol: str
    namespace: str
    path: str


# ------------------------------------------------------------------------------
# Data loader for fetching a File's related entity
# ------------------------------------------------------------------------------


@strawberry.input
class EntityWhereClause(TypedDict):
    """
    Supported where clause fields for the Entity type.
    """

    id: UUIDComparators | None
    entity_id: typing.Optional[UUIDComparators] | None
    producing_run_id: IntComparators | None
    owner_user_id: IntComparators | None
    collection_id: IntComparators | None


@strawberry.field(extensions=[DependencyExtension()])
async def load_entities(
    root: "File",
    info: Info,
    where: EntityWhereClause | None = None,
) -> typing.Optional[typing.Annotated["Entity", strawberry.lazy("api.types.entities")]]:
    """
    Dataloader to fetch related entities, given file IDs.
    """
    dataloader = info.context["sqlalchemy_loader"]
    mapper = inspect(db.File)
    relationship = mapper.relationships["entity"]
    return await dataloader.loader_for(relationship, where).load(root.entity_id)  # type:ignore


# ------------------------------------------------------------------------------
# Main types/inputs
# ------------------------------------------------------------------------------


@strawberry.type
class File:
    """
    GraphQL File type and fields.
    """

    id: strawberry.ID
    entity_id: strawberry.ID
    entity_field_name: str
    entity: typing.Optional[typing.Annotated["Entity", strawberry.lazy("api.types.entities")]] = load_entities
    status: FileStatus
    protocol: str
    namespace: str
    path: str
    file_format: str
    compression_type: typing.Optional[int] = None
    size: typing.Optional[int] = None

    @strawberry.field(extensions=[DependencyExtension()])
    def download_link(
        self,
        expiration: int = 3600,
        s3_client: S3Client = Depends(get_s3_client),
    ) -> typing.Optional[SignedURL]:
        """
        Generate a signed URL for downloading a file from S3.
        """
        if not self.path:  # type: ignore
            return None
        key = self.path  # type: ignore
        bucket_name = self.namespace  # type: ignore
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object", Params={"Bucket": bucket_name, "Key": key}, ExpiresIn=expiration
        )
        return SignedURL(url=url, protocol="https", method="get", expiration=expiration)


@strawberry.type
class MultipartUploadResponse:
    """
    Return type for the uploadFile mutation.
    """

    credentials: MultipartUploadCredentials
    file: File


@strawberry.input
class FileWhereClause(TypedDict):
    """
    Supported where clause fields for the File type.
    """

    id: typing.Optional[UUIDComparators]
    entity_id: typing.Optional[UUIDComparators]
    entity_field_name: typing.Optional[StrComparators]
    status: typing.Optional[EnumComparators[FileStatus]]
    protocol: typing.Optional[StrComparators]
    namespace: typing.Optional[StrComparators]
    path: typing.Optional[StrComparators]
    file_format: typing.Optional[StrComparators]
    compression_type: typing.Optional[StrComparators]
    size: typing.Optional[IntComparators]


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_files(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: typing.Optional[FileWhereClause] = None,
) -> typing.Sequence[File]:
    """
    Handles files {} GraphQL queries.
    """
    rows = await get_db_rows(db.File, session, cerbos_client, principal, where, [])
    return rows  # type: ignore


# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------


async def validate_file(
    file: db.File,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    s3_client: S3Client = Depends(get_s3_client),
) -> None:
    """
    Utility function to validate a file against its file format.
    """
    validator = get_validator(file.file_format)
    try:
        file_size = validator.validate(s3_client, file.namespace, file.path)
    except:  # noqa
        file.status = db.FileStatus.FAILED
    else:
        file.status = db.FileStatus.SUCCESS
        file.size = file_size
    await session.commit()


def generate_multipart_upload_token(
    new_file: db.File,
    expiration: int = 3600,
    sts_client: STSClient = Depends(get_sts_client),
) -> MultipartUploadCredentials:
    """
    Utility function to generate an STS token for multipart upload.
    """
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowSampleUploads",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:CreateMultipartUpload",
                    "s3:AbortMultipartUpload",
                    "s3:ListMultipartUploadParts",
                ],
                "Resource": f"arn:aws:s3:::{new_file.namespace}/{new_file.path}",
            }
        ],
    }

    # Generate an STS token to allow users to
    token_name = f"file-upload-token-{uuid6.uuid7()}"
    creds = sts_client.get_federation_token(Name=token_name, Policy=json.dumps(policy), DurationSeconds=expiration)

    return MultipartUploadCredentials(
        protocol="s3",
        namespace=new_file.namespace,
        path=new_file.path,
        access_key_id=creds["Credentials"]["AccessKeyId"],
        secret_access_key=creds["Credentials"]["SecretAccessKey"],
        session_token=creds["Credentials"]["SessionToken"],
        expiration=creds["Credentials"]["Expiration"].isoformat(),
    )


# ------------------------------------------------------------------------------
# Mutations
# ------------------------------------------------------------------------------


@strawberry.mutation(extensions=[DependencyExtension()])
async def mark_upload_complete(
    file_id: strawberry.ID,
    principal: Principal = Depends(require_auth_principal),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    s3_client: S3Client = Depends(get_s3_client),
) -> db.File:
    """
    Once a file is uploaded, the front-end should make a markUploadComplete mutation
    to mark the file as ready for pipeline analysis.
    """
    query = get_resource_query(principal, cerbos_client, CerbosAction.UPDATE, db.File)
    query = query.filter(db.File.id == file_id)
    file = (await session.execute(query)).scalars().one()
    if not file:
        raise Exception("NOT FOUND!")  # TODO: How do we raise sane errors in our api?

    await validate_file(file, session, s3_client)
    return file


# Need to create separate mutations because they return different types.
# Strawberry is unhappy with a mutation returning a union type.
@strawberry.mutation(extensions=[DependencyExtension()])
async def create_file(
    entity_id: strawberry.ID,
    entity_field_name: str,
    file: FileCreate,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    s3_client: S3Client = Depends(get_s3_client),
    sts_client: STSClient = Depends(get_sts_client),
    settings: APISettings = Depends(get_settings),
) -> db.File:
    """
    Create a file object based on an existing S3 file (no upload).
    """
    new_file = await create_or_upload_file(
        entity_id, entity_field_name, file, -1, session, cerbos_client, principal, s3_client, sts_client, settings
    )
    assert isinstance(new_file, db.File)  # reassure mypy that we're returning the right type
    return new_file


@strawberry.mutation(extensions=[DependencyExtension()])
async def upload_file(
    entity_id: strawberry.ID,
    entity_field_name: str,
    file: FileUpload,
    expiration: int = 3600,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    s3_client: S3Client = Depends(get_s3_client),
    sts_client: STSClient = Depends(get_sts_client),
    settings: APISettings = Depends(get_settings),
) -> MultipartUploadResponse:
    """
    Create a file object and generate an STS token for multipart upload.
    """
    response = await create_or_upload_file(
        entity_id,
        entity_field_name,
        file,
        expiration,
        session,
        cerbos_client,
        principal,
        s3_client,
        sts_client,
        settings,
    )
    assert isinstance(response, MultipartUploadResponse)  # reassure mypy that we're returning the right type
    return response


async def create_or_upload_file(
    entity_id: strawberry.ID,
    entity_field_name: str,
    file: FileCreate | FileUpload,
    expiration: int = 3600,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    s3_client: S3Client = Depends(get_s3_client),
    sts_client: STSClient = Depends(get_sts_client),
    settings: APISettings = Depends(get_settings),
) -> db.File | MultipartUploadResponse:
    """
    Utility function for creating a File object, whether for upload or for linking existing files.
    """
    # Basic validation
    if "/" in file.name:
        raise Exception("File name should not contain /")

    # Fetch the entity if have access to it
    query = get_resource_query(principal, cerbos_client, CerbosAction.UPDATE, db.Entity)
    query = query.filter(db.Entity.id == entity_id)
    entity = (await session.execute(query)).scalars().one()
    if not entity:
        raise Exception("Entity not found")

    # Does that entity type have a column for storing a file ID?
    entity_property_name = f"{entity_field_name}_id"
    if not hasattr(entity, entity_property_name):
        raise Exception(f"This entity does not have a corresponding file of type {entity_field_name}")

    # Unlink the File(s) currently connected to this entity (only commit to DB once add the new File below)
    query = get_resource_query(principal, cerbos_client, CerbosAction.UPDATE, db.File)
    query = query.filter(db.File.entity_id == entity_id)
    query = query.filter(db.File.entity_field_name == entity_field_name)
    current_files = (await session.execute(query)).scalars().all()
    for current_file in current_files:
        current_file.entity_id = None

    # Set file parameters based on user inputs
    file_id = uuid6.uuid7()
    if isinstance(file, FileUpload):
        file_protocol = settings.DEFAULT_UPLOAD_PROTOCOL
        file_namespace = settings.DEFAULT_UPLOAD_BUCKET
        file_path = f"uploads/{file_id}/{file.name}"
    else:
        file_protocol = file.protocol
        file_namespace = file.namespace
        file_path = file.path

    # Create a new file record
    new_file = db.File(
        id=file_id,
        entity_id=entity_id,
        entity_field_name=entity_field_name,
        protocol=file_protocol,
        namespace=file_namespace,
        path=file_path,
        file_format=file.file_format,
        compression_type=file.compression_type,
        status=db.FileStatus.PENDING,
    )
    # Save file to db first
    session.add(new_file)
    await session.commit()
    # Then update entity with file ID (if do both in one transaction, it will fail because of foreign key constraint)
    setattr(entity, entity_property_name, new_file.id)
    await session.commit()

    # If file already exists, validate it
    if isinstance(file, FileCreate):
        await validate_file(new_file, session, s3_client)
        return new_file

    # If new file, create an STS token for multipart upload
    else:
        return MultipartUploadResponse(
            file=new_file,  # type: ignore
            credentials=generate_multipart_upload_token(new_file, expiration, sts_client),
        )


@strawberry.mutation(extensions=[DependencyExtension()])
async def concatenate_files(
    ids: typing.Sequence[uuid.UUID],
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    s3_client: S3Client = Depends(get_s3_client),
    settings: APISettings = Depends(get_settings),
) -> SignedURL:
    """
    Concatenate file contents synchronously. Only use for small files e.g. for exporting small CG FASTAs to Nextclade.
    """
    # FIXME: Check with Product on a reasonable max
    if len(ids) > FILE_CONCATENATION_MAX:
        raise Exception("Cannot concatenate more than 100 files")

    # Get files in question if have access to them
    where = {"id": {"_in": ids}, "status": {"_eq": db.FileStatus.SUCCESS}}
    files = await get_db_rows(db.File, session, cerbos_client, principal, where, [])
    if len(files) < 2:
        raise Exception("Need at least 2 valid files to concatenate")
    for file in files:
        if file.size > FILE_CONCATENATION_MAX_SIZE:
            raise Exception("Cannot concatenate files larger than 1MB")

    # Concatenate files (tmp files are automatically deleted when closed)
    with tempfile.NamedTemporaryFile() as file_concatenated:
        with open(file_concatenated.name, "w") as fp_concat:
            for file in files:
                # Download file locally
                with tempfile.NamedTemporaryFile() as file_temp:
                    s3_client.download_file(file.namespace, file.path, file_temp.name)
                    # Append it
                    with open(file_temp.name) as fp_temp:
                        fp_concat.write(fp_temp.read())
        # Upload to S3
        path = f"{FILE_CONCATENATION_PREFIX}/{uuid6.uuid7()}"
        s3_client.upload_file(file_concatenated.name, file.namespace, path)

    # Return signed URL
    expiration = 36000
    url = s3_client.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": settings.DEFAULT_UPLOAD_BUCKET, "Key": path}, ExpiresIn=expiration
    )
    return SignedURL(url=url, protocol="https", method="get", expiration=expiration)

    # FIXME: tests
    # FIXME: create File object for this? Connected to what?
    # FIXME: custom fasta headers
