"""
Authorization spot-checks
"""

import pytest
from httpx import AsyncClient
from database.connect import SyncDB
from test_infra import factories as fa
import json


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
    http_client: AsyncClient,
):
    # For now, use the hardcoded user_id for tests
    owner_user_id = 333
    user_id = 12345

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SampleFactory.create_batch(
            2, location="City1", owner_user_id=owner_user_id, collection_id=333
        )
        fa.SampleFactory.create_batch(
            2, location="City2", owner_user_id=owner_user_id, collection_id=444
        )
        fa.SampleFactory.create_batch(
            2, location="City3", owner_user_id=owner_user_id, collection_id=555
        )

    # Fetch all samples
    query = """
        query MyQuery {
            samples {
                id,
                location
            }
        }
    """
    request = {"operationName": "MyQuery", "query": query}
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "user_id": str(user_id),
        "member_projects": json.dumps(project_ids),
    }

    result = await http_client.post(
        "/graphql",
        json=request,
        headers=headers,
    )
    output = result.json()
    assert len(output["data"]["samples"]) == num_results
    assert {sample["location"] for sample in output["data"]["samples"]} == set(cities)
