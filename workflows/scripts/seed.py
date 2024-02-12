"""
Seed script to setup db for test data
Imports manifests
"""

import os

import boto3
from botocore.exceptions import ClientError
import factory.random
from sqlalchemy.orm import Session
from settings import APISettings
from platformics.database.connect import init_sync_db
from manifest.manifest import Manifest
from database.models import Workflow, WorkflowVersion
from test_infra.factories.main import SessionStorage
from test_infra.factories.workflow import WorkflowFactory
from test_infra.factories.workflow_version import WorkflowVersionFactory
from test_infra.factories.workflow_run import WorkflowRunFactory


TEST_USER_ID = "111"
TEST_COLLECTION_ID = "444"


def import_manifest(session: Session) -> None:
    boto_endpoint_url = os.getenv("BOTO_ENDPOINT_URL")
    assert boto_endpoint_url is not None, "seed must be run with local AWS infrastructure"

    manifest_file = "/workflows/manifest/test_manifests/simple.yaml"
    with open(manifest_file) as f:
        manifest_str = f.read()
    manifest = Manifest.from_yaml(manifest_str)

    wdl_file = "/workflows/test_workflows/sample_name.wdl"
    s3 = boto3.client("s3", endpoint_url=os.getenv("BOTO_ENDPOINT_URL"))
    try:
        s3.create_bucket(Bucket="local-bucket")
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            pass
        elif e.response["Error"]["Code"] == "BucketAlreadyExists":
            pass
        else:
            raise e
    s3.upload_file(wdl_file, "local-bucket", "sample_name.wdl")

    workflow = session.query(Workflow).filter(Workflow.name == manifest.workflow_name).first()

    if workflow is None:
        workflow = Workflow(
            owner_user_id=TEST_USER_ID,
            collection_id=TEST_COLLECTION_ID,
            name=manifest.workflow_name,
            default_version="1.0.0",
            minimum_supported_version=str("1.0.0"),
        )
        session.add(workflow)
        session.commit()

    workflow_version = WorkflowVersion(
        owner_user_id=TEST_USER_ID,
        collection_id=TEST_COLLECTION_ID,
        graph_json="{}",
        workflow=workflow,
        manifest=manifest_str,
        workflow_uri="s3://local-bucket/sample_name.wdl",
    )
    session.add(workflow_version)
    session.commit()


def use_factoryboy() -> None:
    settings = APISettings.model_validate({})
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    SessionStorage.set_session(session)

    # import manifests
    import_manifest(session=session)

    factory.random.reseed_random(1234567)

    WorkflowFactory.create_batch(4)

    WorkflowVersionFactory.create()

    WorkflowRunFactory.create_batch(5)
    session.commit()


if __name__ == "__main__":
    use_factoryboy()
