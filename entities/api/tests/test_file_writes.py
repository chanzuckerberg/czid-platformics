import os
import pytest
from api.conftest import GQLTestClient
from platformics.database.connect import SyncDB
from test_infra import factories as fa
from mypy_boto3_s3.client import S3Client
from database.models import File
import sqlalchemy as sa


# Test that we can mark a file upload as complete
@pytest.mark.asyncio
async def test_file_validation(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
    moto_client: S3Client,
) -> None:
    user1_id = 12345
    project1_id = 123

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SequencingReadFactory.create(owner_user_id=user1_id, collection_id=project1_id)
        fa.FileFactory.update_file_ids()
        session.commit()
        file = session.execute(sa.select(File)).scalars().one()

    valid_fastq_file = "test_infra/fixtures/test1.fastq"
    moto_client.put_object(Bucket=file.namespace, Key=file.path.lstrip("/"), Body=open(valid_fastq_file, "rb"))

    # Mark upload complete
    query = f"""
      mutation MyMutation {{
        markUploadComplete(fileId: "{file.id}") {{
          id
          namespace
          size
          status
        }}
      }}
    """
    res = await gql_client.query(query, member_projects=[project1_id])
    fileinfo = res["data"]["markUploadComplete"]
    assert fileinfo["status"] == "SUCCESS"
    assert fileinfo["size"] == os.stat(valid_fastq_file).st_size


# Test that invalid fastq's don't work
@pytest.mark.asyncio
async def test_invalid_fastq(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
    moto_client: S3Client,
) -> None:
    user1_id = 12345
    project1_id = 123

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SequencingReadFactory.create(owner_user_id=user1_id, collection_id=project1_id)
        fa.FileFactory.update_file_ids()
        session.commit()
        file = session.execute(sa.select(File)).scalars().one()

    moto_client.put_object(Bucket=file.namespace, Key=file.path.lstrip("/"), Body="this is not a fastq file")

    # Mark upload complete
    query = f"""
      mutation MyMutation {{
        markUploadComplete(fileId: "{file.id}") {{
          id
          namespace
          size
          status
        }}
      }}
    """
    res = await gql_client.query(query, member_projects=[project1_id])
    fileinfo = res["data"]["markUploadComplete"]
    assert fileinfo["status"] == "FAILED"
