"""
Tests for nested queries + authorization
"""

import base64
import pytest
from platformics.database.connect import SyncDB
from collections import defaultdict
from test_infra.factories.main import SessionStorage
from test_infra.factories.sample import SampleFactory
from test_infra.factories.sequencing_read import SequencingReadFactory
from api.conftest import GQLTestClient


@pytest.mark.asyncio
async def test_nested_query(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    # For now, use the hardcoded user_id for tests
    user1_id = 111
    user2_id = 222
    user3_id = 222
    project1_id = 888
    project2_id = 999

    # Create mock data
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        # create some samples with multiple SequencingReads
        sa1 = SampleFactory(owner_user_id=user1_id, collection_id=project1_id)
        sa2 = SampleFactory(owner_user_id=user3_id, collection_id=project1_id)
        sa3 = SampleFactory(owner_user_id=user2_id, collection_id=project2_id)

        seq1 = SequencingReadFactory.create_batch(
            3, sample=sa1, owner_user_id=sa1.owner_user_id, collection_id=sa1.collection_id
        )
        seq2 = SequencingReadFactory.create_batch(
            2,
            sample=sa2,
            owner_user_id=sa2.owner_user_id,
            collection_id=sa2.collection_id,
        )
        seq3 = SequencingReadFactory.create_batch(
            2,
            sample=sa3,
            owner_user_id=sa3.owner_user_id,
            collection_id=sa3.collection_id,
        )

    # Fetch samples and nested sequencing reads AND nested samples again!
    query = """
        query MyQuery {
          samples (where: { name: { _ilike: "Sample%" } }) {
            id
            name
            collectionLocation
            ownerUserId
            collectionId
            sequencingReads(where: { collectionId: { _eq: 888 } }) {
              edges {
                node {
                  collectionId
                  ownerUserId
                  protocol
                  nucleicAcid
                  sample {
                    id
                    ownerUserId
                    collectionId
                    name
                    sequencingReads {
                      edges {
                        node {
                          protocol
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
    """

    # Make sure user1 can only see samples from project1
    results = await gql_client.query(query, user_id=user1_id, member_projects=[project1_id])
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
    # FIXME
    for sample in results["data"]["samples"]:
        assert sample["collectionId"] == project1_id
        actual_samples_by_owner[sample["ownerUserId"]] += 1
        actual_sequences_by_owner[sample["ownerUserId"]] = len(sample["sequencingReads"]["edges"])
        assert sample["sequencingReads"]["edges"][0]["node"]["sample"]["id"] == sample["id"]

    for userid in expected_sequences_by_owner:
        assert actual_sequences_by_owner[userid] == expected_sequences_by_owner[userid]
    for userid in expected_samples_by_owner:
        assert actual_samples_by_owner[userid] == expected_samples_by_owner[userid]


@pytest.mark.asyncio
async def test_relay_node_queries(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    # Create mock data
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        sample = SampleFactory(owner_user_id=111, collection_id=888)
        entity_id = sample.entity_id

        node_id = f"Sample:{entity_id}".encode("ascii")
        node_id_base64 = base64.b64encode(node_id).decode("utf-8")

    # Fetch sample by node ID
    query = f"""
        query MyQuery {{
          node(id: "{node_id_base64}") {{
            ... on Sample {{
              name
              collectionLocation
            }}
          }}
        }}
    """

    results = await gql_client.query(query, user_id=111, member_projects=[888])
    assert results["data"]["node"]["name"] == sample.name
