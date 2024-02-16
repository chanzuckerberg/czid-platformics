import os
import shutil
import tempfile
import urllib.request
from os.path import join
from typing import TypeVar
from urllib.parse import urlparse

from ..settings import CLISettings
from ..database.connect import init_sync_db
from ..database.models.base import Entity

import boto3
from botocore.client import Config

TEST_USER_ID = "111"
TEST_COLLECTION_ID = "444"
LOCAL_BUCKET = "local-bucket"

DEFAULT_WORKFLOW_VERSIONS = {
    "consensus-genome": "3.4.17",
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

    def __enter__(self):
        return self.temp_file

    def __exit__(self, exc_type, exc_val, exc_tb):
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
    def __init__(self):
        self.settings = CLISettings.model_validate({})
        self.app_db = init_sync_db(self.settings.SYNC_DB_URI)
        self.session = self.app_db.session()
        self.query = self.session.query
        self.add = self.session.add
        self.commit = self.session.commit
        self.flush = self.session.flush
        self.s3_local = boto3.client('s3', endpoint_url=os.getenv("BOTO_ENDPOINT_URL"), config=Config(s3={'addressing_style': 'path'}))
        self.upsert_bucket(LOCAL_BUCKET)

    def upsert_bucket(self, bucket_name: str):
        if any(bucket["Name"] == bucket for bucket in self.s3_local.list_buckets().get("Buckets", [])):
            return
        self.s3_local.create_bucket(Bucket=bucket_name)

    def transfer_to_local(self, s3_path: str) -> None:
        """
        Transfers public S3 objects to the local bucket
        """
        parsed = urlparse(s3_path)
        bucket, key = parsed.netloc, parsed.path.lstrip("/")
        self.upsert_bucket(bucket)

        if self.s3_local.list_objects_v2(Bucket=bucket, Prefix=key)["KeyCount"] > 0:
            return

        with TempHTTPFile(f"https://{bucket}.s3.amazonaws.com/{key}") as f:
            self.s3_local.upload_file(f.name, bucket, key)

    T = TypeVar('T', bound=Entity)
    def create_or_fetch_entity(self, entity_type: type[T], **kwargs) -> T:
        entity = self.session.query(entity_type).filter_by(**kwargs).first() or entity_type()
        entity.owner_user_id = TEST_USER_ID
        entity.collection_id = TEST_COLLECTION_ID
        for name, value in kwargs.items():
            setattr(entity, name, value)
        return entity

    def transfer_wdl(self, wdl_name: str, workflow: str, version: str | None = None) -> str:
        key = f"{_workflow_tag(workflow, version)}/{wdl_name}"
        with TempHTTPFile(f"https://idseq-workflows.s3.amazonaws.com/{key}") as f:
          self.s3_local.upload_file(f.name, LOCAL_BUCKET, key)
        return f"s3://{LOCAL_BUCKET}/{key}"

