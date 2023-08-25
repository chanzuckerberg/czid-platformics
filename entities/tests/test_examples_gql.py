"""
GraphQL tests
"""

import json
import pytest
from httpx import AsyncClient
from database.connect import SyncDB
from test_infra import factories as fa

# Utility function for making GQL HTTP queries
@pytest.mark.asyncio
async def query_gql(
    query: str,
    http_client: AsyncClient,
    headers: dict = {}
):
    gql_headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "user_id": "111",
        **headers,
    }
    result = await http_client.post("/graphql", json={"query": query}, headers=gql_headers)
    return result.json()

# Test that we can only fetch samples from the database that we have access to
@pytest.mark.asyncio
async def test_graphql_query(
    sync_db: SyncDB,
    http_client: AsyncClient,
):
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
    output = await query_gql(query, http_client, headers={"member_projects": json.dumps(project_id)})
    locations = [sample["location"] for sample in output["data"]["samples"]]
    assert "San Francisco, CA" in locations
    assert "Mountain View, CA" in locations
    assert "Phoenix, AZ" not in locations


# Validate that can only create/modify samples in collections the user has access to
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "projects_allowed",
    [([123]), ([123])],
)
async def test_graphql_mutations(
    projects_allowed: list[int],
    http_client: AsyncClient,
):
    project_id = 123
    query = """
        mutation myMutation {
            createSample(name: "Test Sample", location: "San Francisco, CA", collectionId: 123) {
                id,
                location
            }
        }
    """
    output = await query_gql(query, http_client, headers={"member_projects": json.dumps(projects_allowed)})

    # Create sample
    if project_id in projects_allowed:
        print("project_id", project_id, projects_allowed, "allowed", output["data"])
        assert output["data"]["createSample"]["location"] == "San Francisco, CA"
    else:
        print("project_id", project_id, projects_allowed, "NOTallowed", output["data"])
        assert output["data"] is None
        assert "Unauthorized" in output["errors"][0]["message"]
