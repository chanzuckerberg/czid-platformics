"""
GraphQL tests
"""

import pytest
from database.connect import SyncDB
from test_infra import factories as fa
from api.conftest import GQLTestClient


# Test that we can only fetch samples from the database that we have access to
@pytest.mark.asyncio
async def test_graphql_query(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
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
    output = await gql_client.query(query, user_id=user_id, member_projects=[project_id])
    locations = [sample["location"] for sample in output["data"]["samples"]]
    assert "San Francisco, CA" in locations
    assert "Mountain View, CA" in locations
    assert "Phoenix, AZ" not in locations


# Validate that can only create/modify samples in collections the user has access to
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "projects_allowed",
    [[123], [456]],
)
async def test_graphql_mutations(
    projects_allowed: list[int],
    gql_client: GQLTestClient,
):
    project_id = 123
    query = """
        mutation createOneSample {
            createSample(name: "Test Sample", location: "San Francisco, CA", collectionId: 123) {
                id,
                location
            }
        }
    """
    output = await gql_client.query(query, member_projects=projects_allowed)

    # Make sure unauthorized users can't create samples in this collection
    if project_id not in projects_allowed:
        assert output["data"] is None
        assert "Unauthorized" in output["errors"][0]["message"]

    # Otherwise, modify the sample we created (note the {{ so we don't treat them as variables)
    else:
        assert output["data"]["createSample"]["location"] == "San Francisco, CA"

        new_location = "Chicago, IL"
        query = f"""
            mutation modifyOneSample {{
                updateSample(entityId: "{output["data"]["createSample"]["id"]}", location: "{new_location}") {{
                    id,
                    location
                }}
            }}
        """
        output = await gql_client.query(query, member_projects=projects_allowed)
        assert output["data"]["updateSample"]["location"] == new_location
