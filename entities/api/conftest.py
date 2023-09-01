import json
import typing
from typing import Optional

import pytest_asyncio
from cerbos.sdk.model import Principal
from database.connect import AsyncDB
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from api.core.deps import get_auth_principal, get_db_session, get_engine, require_auth_principal
from api.main import get_app


class GQLTestClient:
    def __init__(self, http_client: AsyncClient):
        self.http_client = http_client

    # Utility function for making GQL HTTP queries
    async def query(
        self,
        query: str,
        user_id: Optional[int] = None,
        member_projects: Optional[list[int]] = None,
        admin_projects: Optional[list[int]] = None,
    ):
        if not user_id:
            user_id = 111
        if not admin_projects:
            admin_projects = []
        if not member_projects:
            member_projects = []
        gql_headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "user_id": str(user_id),
            "member_projects": json.dumps(member_projects),
            "admin_projects": json.dumps(admin_projects),
        }
        result = await self.http_client.post("/graphql", json={"query": query}, headers=gql_headers)
        return result.json()


@pytest_asyncio.fixture()
async def gql_client(http_client: AsyncClient) -> GQLTestClient:
    client = GQLTestClient(http_client)
    return client


async def patched_authprincipal(request: Request) -> Principal:
    user_id = request.headers.get("user_id")
    if not user_id:
        raise Exception("user_id not found in request headers")
    principal = Principal(
        user_id,
        roles=["user"],
        attr={
            "user_id": int(user_id),
            "member_projects": json.loads(request.headers.get("member_projects", "[]")),
            "admin_projects": json.loads(request.headers.get("admin_projects", "[]")),
        },
    )
    return principal


@pytest_asyncio.fixture()
async def api(
    async_db: AsyncDB,
) -> FastAPI:
    async def patched_session() -> typing.AsyncGenerator[AsyncSession, None]:
        session = async_db.session()
        try:
            yield session
        finally:
            await session.close()

    api = get_app()
    api.dependency_overrides[get_engine] = lambda: async_db
    api.dependency_overrides[get_db_session] = patched_session
    api.dependency_overrides[require_auth_principal] = patched_authprincipal
    api.dependency_overrides[get_auth_principal] = patched_authprincipal
    return api


@pytest_asyncio.fixture()
async def http_client(api: FastAPI) -> AsyncClient:
    return AsyncClient(app=api, base_url="http://test")
