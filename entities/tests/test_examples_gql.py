"""
Example GraphQL test
"""

import pytest
from api.main import schema

@pytest.mark.asyncio
async def test_graphql_query():
    query = """
        query MyQuery {
            getAllSamples {
                id,
                location
            }
        }
    """

    result = await schema.execute(query)
    assert result.errors is None
    assert result.data["getAllSamples"][0] == { "id": 1, "location": "North Bonnie" }
