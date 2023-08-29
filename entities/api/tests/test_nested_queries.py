"""
Tests for nested queries + authorization
"""

import pytest
from httpx import AsyncClient
from database.connect import SyncDB
import json
from collections import defaultdict
from test_infra import factories as fa


async def get_gql_results(
    http_client: AsyncClient, query: str, project_ids: list[int], user_id: int, query_name: str = "MyQuery"
):
    request = {"operationName": query_name, "query": query}
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "member_projects": json.dumps(project_ids),
        "user_id": str(user_id),
    }
    result = await http_client.post(
        "/graphql",
        json=request,
        headers=headers,
    )
    output = result.json()
    return output["data"]


@pytest.mark.asyncio
async def test_nested_query(
    sync_db: SyncDB,
    http_client: AsyncClient,
):
    # For now, use the hardcoded user_id for tests
    user1_id = 111
    user2_id = 222
    user3_id = 222
    project1_id = 888
    project2_id = 999

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        # create some samples with multiple SequencingReads
        sa1 = fa.SampleFactory(owner_user_id=user1_id, collection_id=project1_id)
        sa2 = fa.SampleFactory(owner_user_id=user3_id, collection_id=project1_id)
        sa3 = fa.SampleFactory(owner_user_id=user2_id, collection_id=project2_id)

        seq1 = fa.SequencingReadFactory.create_batch(
            3, sample=sa1, owner_user_id=sa1.owner_user_id, collection_id=sa1.collection_id
        )
        seq2 = fa.SequencingReadFactory.create_batch(
            2,
            sample=sa2,
            owner_user_id=sa2.owner_user_id,
            collection_id=sa2.collection_id,
        )
        seq3 = fa.SequencingReadFactory.create_batch(
            2,
            sample=sa3,
            owner_user_id=sa3.owner_user_id,
            collection_id=sa3.collection_id,
        )

    # Fetch samples and nested sequencing reads AND nested samples again!
    query = """
        query MyQuery {
          samples {
            id
            name
            ownerUserId
            collectionId
            sequencingReads {
              edges {
                node {
                  collectionId
                  ownerUserId
                  sequence
                  nucleotide
                  sample {
                    id
                    ownerUserId
                    collectionId
                    name
                  }
                }
              }
            }
          }
        }
    """

    # Make sure user1 can only see samples from project1
    results = await get_gql_results(http_client, query, [project1_id], user1_id)
    expected_samples_by_owner = {
        user1_id: 1,
        user2_id: 1,
        user3_id: 1,
    }
    expected_sequences_by_owner = {
        user1_id: len(seq1),
        user2_id: len(seq3),
        user3_id: len(seq2),
    }
    actual_samples_by_owner: dict[int, int] = defaultdict(int)
    actual_sequences_by_owner: dict[int, int] = defaultdict(int)
    for sample in results["samples"]:
        assert sample["collectionId"] == project1_id
        actual_samples_by_owner[sample["ownerUserId"]] += 1
        actual_sequences_by_owner[sample["ownerUserId"]] = len(sample["sequencingReads"]["edges"])
        assert sample["sequencingReads"]["edges"][0]["node"]["sample"]["id"] == sample["id"]

    for userid in expected_sequences_by_owner:
        assert actual_sequences_by_owner[userid] == expected_sequences_by_owner[userid]
    for userid in expected_samples_by_owner:
        assert actual_samples_by_owner[userid] == expected_samples_by_owner[userid]
