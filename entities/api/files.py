import typing

import database.models as db
import strawberry
from fastapi import Depends
from platformics.api.core.deps import get_settings
from platformics.api.core.settings import APISettings
from platformics.api.core.strawberry_extensions import DependencyExtension
import boto3
from botocore.client import Config
from api.strawberry import strawberry_sqlalchemy_mapper


@strawberry.type
class SignedURL:
    url: str
    protocol: str
    method: str
    expiration: int


@strawberry_sqlalchemy_mapper.type(db.File)
class File:
    @strawberry.field(extensions=[DependencyExtension()])
    def download_link(
        self, expiration: int = 3600, settings: APISettings = Depends(get_settings)
    ) -> typing.Optional[SignedURL]:
        if not self.path:  # type: ignore
            return None
        key = self.path  # type: ignore
        bucket_name = self.namespace  # type: ignore
        s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            endpoint_url=settings.BOTO_ENDPOINT_URL,
            config=Config(signature_version="s3v4"),
        )
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object", Params={"Bucket": bucket_name, "Key": key}, ExpiresIn=expiration
        )
        return SignedURL(url=url, protocol="https", method="get", expiration=expiration)
