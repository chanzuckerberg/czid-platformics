"""
Example GraphQL test
"""

import pytest
from httpx import AsyncClient
from database.connect import SyncDB
from test_infra import factories as fa

@pytest.mark.asyncio
async def test_graphql_query(
    sync_db: SyncDB,
    http_client: AsyncClient,
):
    # For now, use the hardcoded user_id for tests
    user_id = 12345
    secondary_user_id = 67890

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SampleFactory.create_batch(2, location="San Francisco, CA", owner_user_id=user_id)
        fa.SampleFactory.create_batch(6, location="Mountain View, CA", owner_user_id=user_id)
        fa.SampleFactory.create_batch(4, location="Phoenix, AZ", owner_user_id=secondary_user_id)

    # Fetch all samples
    query = """
        query MyQuery {
            getAllSamples {
                id,
                location
            }
        }
    """
    request = {"operationName": "MyQuery", "query": query}
    headers = {"content-type": "application/json",
               "accept": "application/json",
               "user_id": str(user_id)}
    result = await http_client.post(
        "/graphql",
        json=request,
        headers=headers,
    )
    output = result.json()
    assert output["data"]["getAllSamples"][0] == { "id": 1, "location": "San Francisco, CA" }
    assert output["data"]["getAllSamples"][-1]["location"] == "Mountain View, CA"
    assert len(output["data"]["getAllSamples"]) == 8
