"""
Fixtures for API tests
"""

import json
import typing
from typing import Optional

import boto3
import pytest_asyncio
from cerbos.sdk.model import Principal
from fastapi import FastAPI
from httpx import AsyncClient
from mypy_boto3_s3.client import S3Client
from platformics.api.core.deps import (
    get_auth_principal,
    get_db_session,
    get_engine,
    get_s3_client,
    require_auth_principal,
)
from platformics.database.connect import AsyncDB
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from api.main import get_app


class GQLTestClient:
    def __init__(self, http_client: AsyncClient):
        self.http_client = http_client

    async def query(
        self,
        query: str,
        user_id: Optional[int] = None,
        member_projects: Optional[list[int]] = None,
        owner_projects: Optional[list[int]] = None,
        viewer_projects: Optional[list[int]] = None,
        service_identity: Optional[str] = None,
    ) -> dict[str, typing.Any]:
        """
        Utility function for making GQL HTTP queries with authorization info.
        """
        if not user_id:
            user_id = 111
        if not owner_projects:
            owner_projects = []
        if not member_projects:
            member_projects = []
        if not viewer_projects:
            viewer_projects = []
        gql_headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "user_id": str(user_id),
            "member_projects": json.dumps(member_projects),
            "owner_projects": json.dumps(owner_projects),
            "viewer_projects": json.dumps(viewer_projects),
            "service_identity": service_identity or "",
        }
        result = await self.http_client.post("/graphql", json={"query": query}, headers=gql_headers)
        return result.json()


async def patched_s3_client() -> typing.AsyncGenerator[S3Client, None]:
    yield boto3.client("s3")


@pytest_asyncio.fixture()
async def gql_client(http_client: AsyncClient) -> GQLTestClient:
    """
    Create a GQL client.
    """
    client = GQLTestClient(http_client)
    return client


async def patched_authprincipal(request: Request) -> Principal:
    """
    Create a Principal object from request headers.
    """
    user_id = request.headers.get("user_id")
    if not user_id:
        raise Exception("user_id not found in request headers")
    principal = Principal(
        user_id,
        roles=["user"],
        attr={
            "user_id": int(user_id),
            "member_projects": json.loads(request.headers.get("member_projects", "[]")),
            "owner_projects": json.loads(request.headers.get("owner_projects", "[]")),
            "viewer_projects": json.loads(request.headers.get("viewer_projects", "[]")),
            "service_identity": request.headers.get("service_identity"),
        },
    )
    return principal


def overwrite_api(api: FastAPI, async_db: AsyncDB) -> None:
    """
    Utility function for overwriting API dependencies with test versions.
    """

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
    """
    Create an API instance using the real schema.
    """
    api = get_app()
    overwrite_api(api, async_db)
    return api


@pytest_asyncio.fixture()
async def http_client(api: FastAPI) -> AsyncClient:
    """
    Create an HTTP client.
    """
    return AsyncClient(app=api, base_url="http://test")
