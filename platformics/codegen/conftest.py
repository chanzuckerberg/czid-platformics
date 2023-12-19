import pytest_asyncio
from platformics.database.connect import AsyncDB
from fastapi import FastAPI
from httpx import AsyncClient
import strawberry
from api.conftest import overwrite_api, gql_client, moto_client, GQLTestClient
from platformics.codegen.tests.output.api.queries import Query as QueryCodeGen
from platformics.codegen.tests.output.api.mutations import Mutation as MutationCodeGen
from test_infra.factories.main import SessionStorage, FileFactory
from platformics.api.setup import get_app, get_strawberry_config

__all__ = ["gql_client", "moto_client", "GQLTestClient", "SessionStorage", "FileFactory"]  # needed by tests



@pytest_asyncio.fixture()
async def api_test_schema(async_db: AsyncDB) -> FastAPI:
    strawberry_config = get_strawberry_config()
    schema_test = strawberry.Schema(query=QueryCodeGen, mutation=MutationCodeGen, config=strawberry_config)
    api = get_app(schema_test, title="Codegen Tests")
    overwrite_api(api, async_db)
    return api


# When importing `gql_client`, it will use the `http_client` below, which uses the test schema
@pytest_asyncio.fixture()
async def http_client(api_test_schema: FastAPI) -> AsyncClient:
    return AsyncClient(app=api_test_schema, base_url="http://test-codegen")
