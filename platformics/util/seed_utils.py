import os
import shutil
import tempfile
from types import TracebackType
import urllib.request
from os.path import join
from typing import Any, TypeVar
from urllib.parse import urlparse

from ..settings import CLISettings
from ..database.connect import init_sync_db
from ..database.models.base import Entity

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

TEST_USER_ID = 111
TEST_COLLECTION_ID = 444
LOCAL_BUCKET = "local-bucket"

DEFAULT_WORKFLOW_VERSIONS = {
    "consensus-genome": "3.5.0",
    "bulk-download": "0.0.4",
}


def _workflow_tag(workflow: str, version: str | None = None) -> str:
    return f"{workflow}-v{version or DEFAULT_WORKFLOW_VERSIONS[workflow]}"


class TempHTTPFile:
    def __init__(self, url: str):
        self.url = url
        self.temp_file = tempfile.NamedTemporaryFile()
        with urllib.request.urlopen(url) as response:
            shutil.copyfileobj(response, self.temp_file)
            self.temp_file.seek(0)

    def __enter__(self) -> tempfile._TemporaryFileWrapper:
        return self.temp_file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.temp_file.__exit__(exc_type, exc_val, exc_tb)


class TempGitHubFile(TempHTTPFile):
    def __init__(self, organization: str, repo: str, ref: str, path: str):
        url = f"https://raw.githubusercontent.com/{organization}/{repo}/{ref}/{path}"
        super().__init__(url)


class TempCZIDWorkflowFile(TempGitHubFile):
    def __init__(self, path: str, workflow: str, version: str | None = None, branch: str | None = None):
        super().__init__(
            "chanzuckerberg",
            "czid-workflows",
            branch or _workflow_tag(workflow, version),
            join("workflows", workflow, path),
        )


class SeedSession:
    def __init__(self) -> None:
        self.settings = CLISettings.model_validate({})
        self.app_db = init_sync_db(self.settings.SYNC_DB_URI)
        self.session = self.app_db.session()
        self.query = self.session.query
        self.add = self.session.add
        self.commit = self.session.commit
        self.flush = self.session.flush
        self.s3_local = (
            boto3.client(
                "s3", endpoint_url=os.getenv("BOTO_ENDPOINT_URL"), config=Config(s3={"addressing_style": "path"})
            )
            if os.getenv("BOTO_ENDPOINT_URL")
            else None
        )
        self.upsert_bucket(LOCAL_BUCKET)

    def upsert_bucket(self, bucket_name: str) -> None:
        if not self.s3_local:
            return
        try:
            self.s3_local.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            # Check if the error was because the bucket already exists or is owned by another account
            if e.response["Error"]["Code"] in ("BucketAlreadyExists", "BucketAlreadyOwnedByYou"):
                pass  # Bucket already exists, handle as needed
            else:
                raise e

    def transfer_to_local(self, s3_path: str) -> None:
        """
        Transfers public S3 objects to the local bucket
        """
        if not self.s3_local:
            return
        parsed = urlparse(s3_path)
        bucket, key = parsed.netloc, parsed.path.lstrip("/")
        self.upsert_bucket(bucket)

        if self.s3_local.list_objects_v2(Bucket=bucket, Prefix=key)["KeyCount"] > 0:
            return

        with TempHTTPFile(f"https://{bucket}.s3.amazonaws.com/{key}") as f:
            self.s3_local.upload_file(f.name, bucket, key)

    T = TypeVar("T", bound=Entity)

    def create_or_fetch_entity(self, entity_type: type[T], **kwargs: Any) -> T:
        entity = self.session.query(entity_type).filter_by(**kwargs).first() or entity_type()
        entity.owner_user_id = TEST_USER_ID
        entity.collection_id = TEST_COLLECTION_ID
        for name, value in kwargs.items():
            setattr(entity, name, value)
        return entity

    def transfer_wdl(self, wdl_name: str, workflow: str, version: str | None = None) -> str:
        key = f"{_workflow_tag(workflow, version)}/{wdl_name}"
        if not self.s3_local:
            return f"s3://idseq-workflows/{key}"
        with TempHTTPFile(f"https://idseq-workflows.s3.amazonaws.com/{key}") as f:
            self.s3_local.upload_file(f.name, LOCAL_BUCKET, key)
        return f"s3://{LOCAL_BUCKET}/{key}"

    def remote_path(self, bucket: str, key: str) -> str:
        """
        Returns a path to remote a remote S3 object

        If we are using local S3 it returns an https path to ensure you are using the remote object
        """
        if not self.s3_local:
            return f"s3://{bucket}/{key}"
        return f"https://{bucket}.s3.amazonaws.com/{key}"
