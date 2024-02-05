"""
Seed script to setup db for test data
Imports manifests
"""

import os

import boto3
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


def import_manifest(session: Session) -> None:
    manifest_file = "/workflows/manifest/test_manifests/simple.yaml"
    with open(manifest_file) as f:
        manifest_str = f.read()
    manifest = Manifest.from_yaml(manifest_str)

    wdl_file = "/workflows/test_workflows/sample_name.wdl"
    s3 = boto3.client("s3", endpoint_url=os.getenv("BOTO_ENDPOINT_URL"))
    s3.create_bucket(Bucket="local-bucket")
    s3.upload_file(wdl_file, "local-bucket", "sample_name.wdl")

    workflow = session.query(Workflow).filter(Workflow.name == manifest.workflow_name).first()

    if workflow is None:
        workflow = Workflow(
            owner_user_id="1",  # TODO: WHO SHOULD OWN THESE?
            collection_id="1",  #
            name=manifest.workflow_name,
            default_version="1.0.0",
            minimum_supported_version=str("1.0.0"),
        )
        session.add(workflow)
        session.commit()

    workflow_version = WorkflowVersion(
        owner_user_id="111",
        collection_id="444",
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
