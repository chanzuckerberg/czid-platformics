"""
Tests for nested queries + authorization
"""

import base64
import pytest
from collections import defaultdict
from platformics.database.connect import SyncDB
from codegen.conftest import GQLTestClient, SessionStorage
from codegen.tests.output.test_infra.factories.sample import SampleFactory
from codegen.tests.output.test_infra.factories.sequencing_read import SequencingReadFactory


@pytest.mark.asyncio
async def test_nested_query(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    # For now, use the hardcoded user_id for tests
    user1_id = 111
    user2_id = 222
    project1_id = 888
    project2_id = 999

    # Create mock data
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        # create some samples with multiple SequencingReads
        sa1 = SampleFactory(owner_user_id=user1_id, collection_id=project1_id)
        sa2 = SampleFactory(owner_user_id=user2_id, collection_id=project1_id)
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
        SequencingReadFactory.create_batch(
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
    expected_sequences_by_owner = {user1_id: len(seq1), user2_id: len(seq2)}
    actual_samples_by_owner: dict[int, int] = defaultdict(int)
    actual_sequences_by_owner: dict[int, int] = defaultdict(int)
    for sample in results["data"]["samples"]:
        assert sample["collectionId"] == project1_id
        actual_samples_by_owner[sample["ownerUserId"]] += 1
        actual_sequences_by_owner[sample["ownerUserId"]] = len(sample["sequencingReads"]["edges"])
        assert sample["sequencingReads"]["edges"][0]["node"]["sample"]["id"] == sample["id"]

    for userid in expected_sequences_by_owner:
        assert actual_sequences_by_owner[userid] == expected_sequences_by_owner[userid]
    for userid in [user1_id, user2_id]:
        assert actual_samples_by_owner[userid] == 1


@pytest.mark.asyncio
async def test_relay_node_queries(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    # Create mock data
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        sample1 = SampleFactory(owner_user_id=111, collection_id=888)
        sample2 = SampleFactory(owner_user_id=111, collection_id=888)
        node1_id = f"Sample:{sample1.entity_id}".encode("ascii")
        node2_id = f"Sample:{sample2.entity_id}".encode("ascii")
        node1_id_base64 = base64.b64encode(node1_id).decode("utf-8")
        node2_id_base64 = base64.b64encode(node2_id).decode("utf-8")

    # Fetch one node
    query = f"""
        query MyQuery {{
          node(id: "{node1_id_base64}") {{
            ... on Sample {{
              name
            }}
          }}
        }}
    """
    results = await gql_client.query(query, user_id=111, member_projects=[888])
    assert results["data"]["node"]["name"] == sample1.name

    # Fetch multiple nodes
    query = f"""
        query MyQuery {{
          nodes(ids: ["{node1_id_base64}", "{node2_id_base64}"]) {{
            ... on Sample {{
              name
            }}
          }}
        }}
    """

    results = await gql_client.query(query, user_id=111, member_projects=[888])
    assert results["data"]["nodes"][1]["name"] == sample2.name
