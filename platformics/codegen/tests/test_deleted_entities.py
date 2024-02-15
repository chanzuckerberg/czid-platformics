"""
Test cascade delete
"""

import os
import pytest
import sqlalchemy as sa
from mypy_boto3_s3.client import S3Client
from platformics.database.connect import SyncDB
from database.models import File, FileStatus
from platformics.codegen.conftest import SessionStorage, FileFactory, GQLTestClient
from platformics.codegen.tests.output.test_infra.factories.sequencing_read import SequencingReadFactory
from platformics.codegen.tests.output.test_infra.factories.sample import SampleFactory
from platformics.codegen.tests.output.database.models import SequencingRead

@pytest.mark.asyncio
async def test_cascade_delete(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
    moto_client: S3Client,
) -> None:
    """
    Test that we can mark a file upload as complete
    """
    user_id = 12345
    project_id = 123
    secondary_project_id = 456

    # Create mock data
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        SampleFactory.create_batch(
            2, collection_location="San Francisco, CA", owner_user_id=user_id, collection_id=project_id
        )
        SampleFactory.create_batch(
            3, collection_location="Mountain View, CA", owner_user_id=user_id, collection_id=secondary_project_id
        )

    # Mark upload complete
    query = f"""
      query MyQuery {{
        sequencingReads {{
          id
        }}
      }}
    """
    result = await gql_client.query(query, member_projects=[project1_id])
    print("RESULT", result)
    d
    # fileinfo = res["data"]["markUploadComplete"]
    # assert fileinfo["status"] == "SUCCESS"
    # assert fileinfo["size"] == file_size
