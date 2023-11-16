"""
TODO: WGS tests
"""

import pytest
from api.conftest import GQLTestClient


# Placeholder test: make sure we querying the real schema, not the mock one
@pytest.mark.asyncio
async def test_wgs_TODO(gql_client: GQLTestClient) -> None:
    query = """
        query MyQuery {
            referenceGenomes {
                id
            }
        }
    """
    output = await gql_client.query(query)
    assert "errors" not in output
