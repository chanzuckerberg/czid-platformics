"""
Example GraphQL test
"""

import pytest
from httpx import AsyncClient
from database.connect import SyncDB
import json
from test_infra import factories as fa


@pytest.mark.asyncio
async def test_graphql_query(
    sync_db: SyncDB,
    http_client: AsyncClient,
):
    # For now, use the hardcoded user_id for tests
    user_id = 12345
    secondary_user_id = 67890
    project_id = 123

    # Create mock data
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        fa.SampleFactory.create_batch(2, location="San Francisco, CA", owner_user_id=user_id, collection_id=project_id)
        fa.SampleFactory.create_batch(6, location="Mountain View, CA", owner_user_id=user_id, collection_id=project_id)
        fa.SampleFactory.create_batch(4, location="Phoenix, AZ", owner_user_id=secondary_user_id, collection_id=9999)

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
        "member_projects": json.dumps([project_id]),
        "user_id": str(user_id),
    }
    result = await http_client.post("/graphql", json=request, headers=headers)
    output = result.json()
    assert output["data"]["samples"][0]["location"] == "San Francisco, CA"
    assert output["data"]["samples"][-1]["location"] == "Mountain View, CA"
    assert len(output["data"]["samples"]) == 8


# Validate that can only create samples in collections the user has access to
@pytest.mark.asyncio
async def test_graphql_create_sample(
    http_client: AsyncClient,
):
    project_id_allowed = 123
    project_id_not_allowed = 456
    query = """
        mutation CreateASample {
            createSample(name: "Test Sample", location: "San Francisco, CA", collectionId: 123) {
                id,
                location
            }
        }
    """
    request = {"operationName": "CreateASample", "query": query}

    for project_id in [project_id_allowed, project_id_not_allowed]:
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "member_projects": json.dumps([project_id]),
            "user_id": "111",
        }
        result = await http_client.post("/graphql", json=request, headers=headers)
        output = result.json()
        if project_id == project_id_allowed:
            assert output["data"]["createSample"]["location"] == "San Francisco, CA"
        else:
            assert output["data"] is None
            assert output["errors"][0]["message"] == "Unauthorized"
