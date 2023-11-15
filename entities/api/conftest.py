import json
import typing
from typing import Optional

import boto3
import pytest_asyncio
from cerbos.sdk.model import Principal
from platformics.database.connect import AsyncDB
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from moto import mock_s3
from mypy_boto3_s3.client import S3Client

from platformics.api.core.deps import (
    get_auth_principal,
    get_db_session,
    get_engine,
    require_auth_principal,
    get_s3_client,
)
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
    ) -> dict[str, typing.Any]:
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
async def moto_client() -> typing.AsyncGenerator[S3Client, None]:
    mocks3 = mock_s3()
    mocks3.start()
    res = boto3.resource("s3")
    res.create_bucket(Bucket="local-bucket")
    res.create_bucket(Bucket="remote-bucket")
    yield boto3.client("s3")
    mocks3.stop()


async def patched_s3_client() -> typing.AsyncGenerator[S3Client, None]:
    yield boto3.client("s3")


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


def overwrite_api(api: FastAPI, async_db: AsyncDB) -> None:
    async def patched_session() -> typing.AsyncGenerator[AsyncSession, None]:
        session = async_db.session()
        try:
            yield session
        finally:
            await session.close()

    api.dependency_overrides[get_engine] = lambda: async_db
    api.dependency_overrides[get_db_session] = patched_session
    api.dependency_overrides[require_auth_principal] = patched_authprincipal
    api.dependency_overrides[get_auth_principal] = patched_authprincipal
    api.dependency_overrides[get_s3_client] = patched_s3_client


@pytest_asyncio.fixture()
async def api(async_db: AsyncDB) -> FastAPI:
    api = get_app(use_test_schema=True)
    overwrite_api(api, async_db)
    return api


@pytest_asyncio.fixture()
async def http_client(api: FastAPI) -> AsyncClient:
    return AsyncClient(app=api, base_url="http://test")
