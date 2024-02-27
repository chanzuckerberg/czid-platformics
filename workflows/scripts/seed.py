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
        secret_value = 'eyJhbGciOiJFQ0RILUVTIiwiZW5jIjoiQTI1NkNCQy1IUzUxMiIsImVwayI6eyJjcnYiOiJQLTM4NCIsImt0eSI6IkVDIiwieCI6Ims2Y01iUUJJVnpCaWotOWtuRF9tR3lCVXo4Q3BTRV9EVUZlMFBnVEFqT1k3Y3N4NFNHQmhXYmMwTzN3bjFQZ0siLCJ5IjoiZ3JqMksxSW5HVFZCZ1lrbFFFUjdUWXVBUmlPTXZTUXplUGZmVWZoa2N5bktFNWVfR0g2bGo4bWpyZE1aUlo0WSJ9LCJraWQiOiItQmx2bF9wVk5LU2JRQ2N5dGV4UzNfMk5MaHBia2J6LVk5VFFjbkY5S1drIiwidHlwIjoiSldFIn0..Uy_6hWYnHrt7j_0evaWnCw.ql9UQ40bXYis_k1NMamaxzVRxFY_FIpRVYz6xPPoBJop_nAlMgTRffn81BbbX98jrLNNYtd9ODwylzHy56iU4ykl6oWUn9Ufvu3EIogWoQUMTJbepcduFITe_J1UvUUGXcgfM4UQpaLpUPZNUzhuxDzmGFY-f5OD31dggyZtFUOGKKU5Oa5NJs6hbat9FOy6Z9zq2j9ycndEGeYZozI3SLTHMzqBv4YjOOf0Bmc3vG63Veer7R3pEMkD2NXUpqyXnTYuozvnzCHFi2Notl972S5GD5pVXCZ5Cju2alT10avHPwPjAs83E79Sgna7h4hKykmdu2CpFN9Cfu2OgdmIbldCLQ0Xaomh4nKSmQnwBCdzaukF-uC6c4qhosrO0V9R-Ie8sTgpZLwCyeuNqxCq4ayx9qyPlUHhUgMHJQJMxsPNd-GBWAI7X_8nmoCYvziU5yz_YG76NoPo4ViiGyj0PLMXePXEW59K_l_EJuyW8VGT--Biap2wxm4tPz7WT3KjPdZbemP4MoPCsj2_5dDgyQ.-s9HRO5yOPRAv69pCAjtK81fDI2cmwe5DT0jzaVaRIY'
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
