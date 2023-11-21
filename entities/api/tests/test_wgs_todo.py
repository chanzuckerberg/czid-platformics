"""
TODO: WGS tests
"""

import pytest
from api.conftest import GQLTestClient


@pytest.mark.asyncio
async def test_wgs_TODO(gql_client: GQLTestClient) -> None:
    """
    Placeholder test: make sure we querying the real schema, not the mock one
    """
    query = """
        query MyQuery {
            referenceGenomes {
                id
            }
        }
    """
    output = await gql_client.query(query)
    assert "errors" not in output
