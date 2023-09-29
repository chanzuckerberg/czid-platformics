import os
import pytest
from api.conftest import GQLTestClient
from platformics.database.connect import SyncDB
from test_infra import factories as fa
from mypy_boto3_s3.client import S3Client
from database.models import File, FileStatus, SequencingRead
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
    file_size = os.stat(valid_fastq_file).st_size
    moto_client.put_object(Bucket=file.namespace, Key=file.path, Body=open(valid_fastq_file, "rb"))

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
    assert fileinfo["size"] == file_size

    # Make sure the file was updated in the database
    with sync_db.session() as session:
        file = session.execute(sa.select(File)).scalars().one()
        assert file.status == FileStatus.SUCCESS
        assert file.size == file_size

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

    moto_client.put_object(Bucket=file.namespace, Key=file.path, Body="this is not a fastq file")

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


# Test creating files
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "member_projects,project_id,entity_field",
    [
        ([456], 123, "sequence_file"),  # Can't create file for entity you don't have access to
        ([123], 123, "does_not_exist"),  # Can't create file for entity that isn't connected to a valid file type
        ([123], 123, "sequence_file"),  # Can create file for entity you have access to
    ],
)
async def test_create_file(
    member_projects: list[int],
    project_id: int,
    entity_field: str,
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    user_id = 12345

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SequencingReadFactory.create(owner_user_id=user_id, collection_id=project_id)
        fa.FileFactory.update_file_ids()
        session.commit()

        sequencing_read = session.execute(sa.select(SequencingRead)).scalars().one()
        entity_id = sequencing_read.entity_id

    # Try creating a file
    mutation = f"""
        mutation MyQuery {{
          createFile(entityId: "{entity_id}", entityFieldName: "{entity_field}",
            fileName: "test.fastq", fileSize: 123, fileFormat: "fastq") {{
            url
            expiration
            method
            protocol
            fields
          }}
        }}
    """
    output = await gql_client.query(mutation, member_projects=member_projects)

    # If don't have access to this entity, or trying to link an entity with a made up file type, should get an error
    if project_id not in member_projects or entity_field == "does_not_exist":
        assert output["data"] is None
        assert output["errors"] is not None
        return

    assert output["data"]["createFile"]["url"] == "https://local-bucket.s3.amazonaws.com/"
