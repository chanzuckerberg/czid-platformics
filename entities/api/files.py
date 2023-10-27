import json
import typing
import database.models as db
import strawberry
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
from strawberry.dataloader import DataLoader
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from platformics.api.core.deps import (
    get_cerbos_client,
    get_db_session,
    require_auth_principal,
    get_settings,
    get_sts_client,
)
from platformics.settings import APISettings
from sqlalchemy.ext.asyncio import AsyncSession
from platformics.security.authorization import CerbosAction, get_resource_query
from files.format_handlers import get_validator
from api.core.helpers import get_db_rows
from api.types.entities import Entity
from database.models import FileStatus


# ------------------------------------------------------------------------------
# Utility types/inputs
# ------------------------------------------------------------------------------


@strawberry.type
class SignedURL:
    url: str
    protocol: str
    method: str
    expiration: int
    fields: typing.Optional[JSON] = None  # type: ignore


@strawberry.type
class MultipartUploadCredentials:
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
    name: str
    file_format: str
    compression_type: typing.Optional[str] = None


@strawberry.input()
class FileCreate:
    name: str
    file_format: str
    compression_type: typing.Optional[str] = None
    protocol: str
    namespace: str
    path: str


# ------------------------------------------------------------------------------
# Data loader for fetching a File's related entity
# ------------------------------------------------------------------------------


def cache_key(key: dict) -> str:
    return key["id"]


async def batch_entities(
    keys: list[dict],
) -> typing.Annotated["Entity", strawberry.lazy("api.types.entities")]:
    session = keys[0]["session"]
    cerbos_client = keys[0]["cerbos_client"]
    principal = keys[0]["principal"]
    file_ids = [key["id"] for key in keys]

    # Infer entity IDs from each file ID
    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.File)
    query = query.filter(db.File.id.in_(file_ids))
    all_files = (await session.execute(query)).scalars().all()
    entity_ids = [file.entity_id for file in all_files]

    # Fetch Entity objects by ID
    query = get_resource_query(principal, cerbos_client, CerbosAction.VIEW, db.Entity)
    query = query.filter(db.Entity.id.in_(entity_ids))
    all_entities = (await session.execute(query)).scalars().all()

    # Group the results by Entity id (each file has exactly one entity it relates to)
    result = []
    for id in entity_ids:
        matching_entities = [e for e in all_entities if e.entity_id == id]
        assert len(matching_entities) == 1
        result.append(matching_entities[0])
    return result


entity_loader = DataLoader(load_fn=batch_entities, cache_key_fn=cache_key)


@strawberry.field(extensions=[DependencyExtension()])
async def load_entities(
    root: "Entity",
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> typing.Annotated["Entity", strawberry.lazy("api.types.entities")]:
    return await entity_loader.load(
        {"session": session, "cerbos_client": cerbos_client, "principal": principal, "id": root.id}
    )


# ------------------------------------------------------------------------------
# Main types/inputs
# ------------------------------------------------------------------------------


@strawberry.type
class File:
    id: uuid.UUID
    entity_id: uuid.UUID
    entity_field_name: str
    entity: typing.Annotated["Entity", strawberry.lazy("api.types.entities")] = load_entities
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
    credentials: MultipartUploadCredentials
    file: File


@strawberry.input
class FileWhereClause(TypedDict):
    id: typing.Optional[UUIDComparators]
    status: typing.Optional[EnumComparators[FileStatus]]
    protocol: typing.Optional[StrComparators]
    namespace: typing.Optional[StrComparators]
    path: typing.Optional[StrComparators]
    compression_type: typing.Optional[StrComparators]
    size: typing.Optional[IntComparators]


@strawberry.field(extensions=[DependencyExtension()])
async def resolve_files(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    where: typing.Optional[FileWhereClause] = None,
) -> typing.Sequence[File]:
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
        protocol="S3",
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
    file_id: uuid.UUID,
    principal: Principal = Depends(require_auth_principal),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    s3_client: S3Client = Depends(get_s3_client),
) -> db.File:
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
    entity_id: uuid.UUID,
    entity_field_name: str,
    file: FileCreate,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    s3_client: S3Client = Depends(get_s3_client),
    sts_client: STSClient = Depends(get_sts_client),
    settings: APISettings = Depends(get_settings),
) -> db.File:
    new_file = await create_or_upload_file(
        entity_id, entity_field_name, file, -1, session, cerbos_client, principal, s3_client, sts_client, settings
    )
    assert isinstance(new_file, db.File)  # reassure mypy that we're returning the right type
    return new_file


@strawberry.mutation(extensions=[DependencyExtension()])
async def upload_file(
    entity_id: uuid.UUID,
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
    entity_id: uuid.UUID,
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
            file=new_file,
            credentials=generate_multipart_upload_token(new_file, expiration, sts_client),
        )
