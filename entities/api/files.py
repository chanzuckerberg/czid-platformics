import typing
import database.models as db
import strawberry
import uuid
import uuid6
from fastapi import Depends
from mypy_boto3_s3.client import S3Client
from platformics.api.core.deps import get_s3_client
from platformics.api.core.strawberry_extensions import DependencyExtension
from api.strawberry import strawberry_sqlalchemy_mapper
from strawberry.scalars import JSON

from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from platformics.api.core.deps import get_cerbos_client, get_db_session, require_auth_principal, get_settings
from platformics.api.core.settings import APISettings
from sqlalchemy.ext.asyncio import AsyncSession
from platformics.security.authorization import CerbosAction, get_resource_query
from files.format_handlers import get_validator


@strawberry.type
class SignedURL:
    url: str
    protocol: str
    method: str
    expiration: int
    fields: typing.Optional[JSON] = None  # type: ignore


# Define graphQL input types so we can pass a file JSON to mutations
@strawberry.input()
class FileUploadInput():
    name: str
    format: str
    compression_type: typing.Optional[str] = None

@strawberry.input()
class FileInput():
    name: str
    format: str
    protocol: str
    namespace: str
    path: str = None
    compression_type: typing.Optional[str] = None


@strawberry_sqlalchemy_mapper.type(db.File)
class File:
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

    validator = get_validator(file.file_format)
    try:
        file_size = validator.validate(s3_client, file.namespace, file.path)
    except:  # noqa
        file.status = db.FileStatus.FAILED
    else:
        file.status = db.FileStatus.SUCCESS
        file.size = file_size
    await session.commit()

    return file


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_file(
    entity_id: uuid.UUID,
    entity_field_name: str,
    file: FileInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> db.File:
    pass

@strawberry.mutation(extensions=[DependencyExtension()])
async def create_file_upload(
    entity_id: uuid.UUID,
    entity_field_name: str,
    file: FileUploadInput,
    expiration: int = 3600,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    s3_client: S3Client = Depends(get_s3_client),
    settings: APISettings = Depends(get_settings),
) -> SignedURL:
    # Set upload destination and create file object
    file.id = uuid6.uuid7()
    file.path = f"uploads/{file.id}/{file.name}"
    file.protocol = settings.DEFAULT_UPLOAD_PROTOCOL
    file.namespace = settings.DEFAULT_UPLOAD_BUCKET
    file = await create_or_upload_file(entity_id, entity_field_name, file, session, cerbos_client, principal)

    # Create a signed URL
    response = s3_client.generate_presigned_post(Bucket=file.namespace, Key=file.path, ExpiresIn=expiration)
    return SignedURL(
        url=response["url"], fields=response["fields"], protocol="https", method="POST", expiration=expiration
    )

async def create_or_upload_file(
    entity_id: uuid.UUID,
    entity_field_name: str,
    file: FileInput | FileUploadInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
):
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

    # Create a new file record
    file = db.File(
        id=file.id,
        entity_id=entity_id,
        entity_field_name=entity_field_name,
        file_format=file.format,
        compression_type=file.compression_type,
        protocol=file.protocol,
        namespace=file.namespace,
        path=file.path,
        status=db.FileStatus.PENDING,
    )
    session.add(file)
    setattr(entity, entity_property_name, file.id)
    await session.commit()

    return file
