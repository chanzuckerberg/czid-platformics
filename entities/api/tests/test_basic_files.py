"""
GraphQL tests
"""

import pytest
from api.conftest import GQLTestClient
from database.connect import SyncDB
from test_infra import factories as fa


# Test that we can only fetch files that we have access to
@pytest.mark.asyncio
async def test_file_query(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    user1_id = 12345
    user2_id = 67890
    user3_id = 87654
    project1_id = 123
    project2_id = 456

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SequencingReadFactory.create_batch(2, owner_user_id=user1_id, collection_id=project1_id)
        fa.SequencingReadFactory.create_batch(6, owner_user_id=user2_id, collection_id=project1_id)
        fa.SequencingReadFactory.create_batch(4, owner_user_id=user3_id, collection_id=project2_id)
        fa.FileFactory.update_file_ids()

    # Fetch all samples
    query = """
        query MyQuery {
        files {
          entity {
            collectionId
            ownerUserId
            id
            type
          }
          path
          entityFieldName
        }
      }
    """
    output = await gql_client.query(query, member_projects=[project1_id])
    assert len(output["data"]["files"]) == 8
    for file in output["data"]["files"]:
        assert file["path"] is not None
        assert file["entity"]["collectionId"] == project1_id
        assert file["entity"]["ownerUserId"] in (user1_id, user2_id)


# Test that we can fetch related file info.
@pytest.mark.asyncio
async def test_nested_files(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    user1_id = 12345
    user2_id = 67890
    user3_id = 87654
    project1_id = 123
    project2_id = 456

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SequencingReadFactory.create_batch(2, owner_user_id=user1_id, collection_id=project1_id)
        fa.SequencingReadFactory.create_batch(6, owner_user_id=user2_id, collection_id=project1_id)
        fa.SequencingReadFactory.create_batch(4, owner_user_id=user3_id, collection_id=project2_id)
        fa.FileFactory.update_file_ids()

    # Fetch all samples
    query = """
        query MyQuery {
          sequencingReads {
            sequenceFile {
              entityId
              fileFormat
              path
              size
            }
            nucleotide
            id
            ownerUserId
          }
        }
    """
    output = await gql_client.query(query, member_projects=[project1_id])
    assert len(output["data"]["sequencingReads"]) == 8
    for read in output["data"]["sequencingReads"]:
        assert read["sequenceFile"] is not None
        assert read["sequenceFile"]["entityId"] == read["id"]
        assert read["sequenceFile"]["path"]
