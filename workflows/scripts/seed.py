"""
Seed script to setup db for test data
Imports manifests
"""

import os
import argparse

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
TEST_BUCKET = "local-bucket"


def upload_wdl() -> None:
    boto_endpoint_url = os.getenv("BOTO_ENDPOINT_URL")
    assert boto_endpoint_url is not None, "seed must be run with local AWS infrastructure"

    wdl_file = "/workflows/test_workflows/sample_name.wdl"
    s3 = boto3.client("s3", endpoint_url=boto_endpoint_url)
    try:
        s3.create_bucket(Bucket=TEST_BUCKET)
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            pass
        elif e.response["Error"]["Code"] == "BucketAlreadyExists":
            pass
        else:
            raise e
    s3.upload_file(wdl_file, TEST_BUCKET, "sample_name.wdl")


def import_manifest(session: Session) -> None:
    manifest_file = "/workflows/manifest/test_manifests/simple.yaml"
    with open(manifest_file) as f:
        manifest_str = f.read()
    manifest = Manifest.from_yaml(manifest_str)

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


def use_factoryboy(use_moto: bool = False) -> None:
    settings = APISettings.model_validate({})
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    SessionStorage.set_session(session)

    if use_moto:
        # upload wdl
        upload_wdl()

        # Initialize a boto3 client
        secrets_manager_client = boto3.client('secretsmanager', endpoint_url=os.environ["BOTO_ENDPOINT_URL"])

        # Specify the secret name and the secret value
        secret_name = os.environ["SERVICE_IDENTITY_SECRET_NAME"]
        secret_value = 'eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTI1NkNCQy1IUzUxMiIsImVwayI6eyJjcnYiOiJQLTM4NCIsImt0eSI6IkVDIiwieCI6ImdQRHd2ZEZFTHpDSXlpakRmbEZnUzZmUEh5bzRuRkU1aGRxZXo3aDN2QUpXWldQT0JYeHdQeXMycHozaWRNalIiLCJ5IjoiaUd1S1dzNmx2SzFrd0hsSEtkcHc3cUI0RVBGWWRQNWJNRUx6cXNFY0FYRXNWaFlHa1dNdFhhTi1EVlBlN1g4SCJ9LCJraWQiOiJ5Y2dLZGxIUW9aNXdDX0dnVWd0alFGZVBCVzFkNFVmaHY5MDJzaTlLRzZRIiwidHlwIjoiSldFIn0..LjTQY6tItUCGPy-d1lmSTA.nlic--8uzG8u-CCH8kHuec6ji3EsTQNjjctTET07ybRbWz6wlw2ddJqhOp9ZEJ-kLHVdvbsVMHuOPkpRjS7_r61lTNkNh-74ZbryYkPcdB-Lni2Psu6xL_NIwgC7rzQs59gLJY61HbvOS4iOD14-tPFuB8gQQp0AGHvygHS3uCtYe56ZxltsDXL10kev6l4FKhlwzWxEO_VAlRVySVcPM0bGHaudiNRiPHbj4lDqex260H32meslV7o91baMRhxnpeinD6buowBZjxuzX52tXH4IEBUos83jFYW-aKokeSyWeDs2CJjm_hWcy8hqjFDLPiB02adEFO0u5yBZXnyhV0k2t8l3Hvly9KjYIZ6EuFEw_B4m6wGsOZr9ZICcjwdy2lgN2xpsfzu-TpOQ_c1EpKGYl9OYIKKLcQ6NdNR2oiTWxn7xouOPf44-IX3zJNvrplTtVJpAzZRQK4tLTMHZ3sh1h1bjlMT3jRQIxz-xbpOu1UlqolQ0egPG-zMUjQ55Q2xxx-4Z0wwLFDDBmXtirQ.YFw9yTh_hmUWNcKeCo076ZwqI9gWMD9D7_j2_rfAXHQ'
        secrets_manager_client.create_secret(
            Name=secret_name,
            SecretString=secret_value
        )
        

    # import manifests
    import_manifest(session=session)

    factory.random.reseed_random(1234567)

    WorkflowFactory.create_batch(4)

    WorkflowVersionFactory.create()

    WorkflowRunFactory.create_batch(5)
    session.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-moto", action="store_true", default=False, help="using moto as aws mock")
    args = parser.parse_args()

    use_factoryboy(args.use_moto)
