"""
Authorization spot-checks
"""

import pytest
from database.connect import SyncDB
from test_infra import factories as fa
from api.conftest import GQLTestClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "project_ids,num_results,cities",
    [([], 0, ()), ([333], 2, {"City1"}), ([333, 555], 4, {"City1", "City3"})],
)
async def test_collection_authorization(
    project_ids: list[int],
    num_results: int,
    cities: tuple[str],
    sync_db: SyncDB,
    gql_client: GQLTestClient,
):
    # For now, use the hardcoded user_id for tests
    owner_user_id = 333
    user_id = 12345

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SampleFactory.create_batch(2, location="City1", owner_user_id=owner_user_id, collection_id=333)
        fa.SampleFactory.create_batch(2, location="City2", owner_user_id=owner_user_id, collection_id=444)
        fa.SampleFactory.create_batch(2, location="City3", owner_user_id=owner_user_id, collection_id=555)

    # Fetch all samples
    query = """
        query MyQuery {
            samples {
                id,
                location
            }
        }
    """
    output = await gql_client.query(query, user_id=user_id, member_projects=project_ids)
    assert len(output["data"]["samples"]) == num_results
    assert {sample["location"] for sample in output["data"]["samples"]} == set(cities)
