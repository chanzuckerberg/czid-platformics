import typing
import database.models as db
import strawberry
from fastapi import Depends
from mypy_boto3_s3.client import S3Client
from platformics.api.core.deps import get_s3_client
from platformics.api.core.strawberry_extensions import DependencyExtension
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
        self,
        expiration: int = 3600,
        s3_client: S3Client = Depends(get_s3_client),
    ) -> typing.Optional[SignedURL]:
        if not self.path:  # type: ignore
            return None
        key = self.path.lstrip("/")  # type: ignore
        bucket_name = self.namespace  # type: ignore
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object", Params={"Bucket": bucket_name, "Key": key}, ExpiresIn=expiration
        )
        return SignedURL(url=url, protocol="https", method="get", expiration=expiration)
