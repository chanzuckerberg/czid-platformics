import pytest_asyncio
from api.conftest import GQLTestClient, gql_client, moto_client, overwrite_api
from api.main import get_app
from fastapi import FastAPI
from httpx import AsyncClient
from platformics.database.connect import AsyncDB
from test_infra.factories.main import FileFactory, SessionStorage

__all__ = ["gql_client", "moto_client", "GQLTestClient", "SessionStorage", "FileFactory"]  # needed by tests


@pytest_asyncio.fixture()
async def api_test_schema(async_db: AsyncDB) -> FastAPI:
    api = get_app()
    overwrite_api(api, async_db)
    return api


# When importing `gql_client`, it will use the `http_client` below, which uses the test schema
@pytest_asyncio.fixture()
async def http_client(api_test_schema: FastAPI) -> AsyncClient:
    return AsyncClient(app=api_test_schema, base_url="http://test-codegen")
