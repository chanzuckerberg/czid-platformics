import pytest_asyncio
from platformics.database.connect import AsyncDB
from fastapi import FastAPI
from httpx import AsyncClient
from api.conftest import overwrite_api, gql_client, moto_client, GQLTestClient
from platformics.codegen.tests.output.api.main import api_schema
from test_infra.factories.main import SessionStorage, FileFactory
from platformics.api.setup import get_app, get_strawberry_config

__all__ = ["gql_client", "moto_client", "GQLTestClient", "SessionStorage", "FileFactory"]  # needed by tests



@pytest_asyncio.fixture()
async def api(async_db: AsyncDB) -> FastAPI:
    api = get_app(api_schema, title="Codegen Tests")
    overwrite_api(api, async_db)
    return api


# When importing `gql_client`, it will use the `http_client` below, which uses the test schema
@pytest_asyncio.fixture()
async def http_client(api: FastAPI) -> AsyncClient:
    return AsyncClient(app=api, base_url="http://test-codegen")
