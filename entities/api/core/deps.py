import typing

from database.connect import AsyncDB, init_async_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from starlette.requests import Request
from api.core.settings import APISettings
from security.token_auth import get_token_claims


def get_settings(request: Request) -> APISettings:
    """Get the settings object from the app state"""
    return request.app.state.entities_settings


async def get_engine(
    settings: APISettings = Depends(get_settings),
) -> typing.AsyncGenerator[AsyncDB, None]:
    """Wrap resolvers in a DB engine"""
    engine = init_async_db(settings.DB_URI)
    try:
        yield engine
    finally:
        pass


async def get_db_session(
    engine: AsyncDB = Depends(get_engine),
) -> typing.AsyncGenerator[AsyncSession, None]:
    """Wrap resolvers in a sqlalchemy-compatible db session"""
    session = engine.session()
    try:
        yield session
    finally:
        await session.close()  # type: ignore


def get_cerbos_client():
    return CerbosClient(host="http://cerbos:3592")


def get_auth_principal(
    request: Request, settings: APISettings = Depends(get_settings)
) -> Principal:
    auth_header = request.headers.get("authorization")
    if auth_header:
        parts = auth_header.split()
    if not auth_header or len(parts) != 2:
        raise Exception("Authorization bearer token is required")
    if parts[0].lower() != "bearer":
        raise Exception("Authorization header must start with Bearer")

    try:
        claims = get_token_claims(settings.JWK_PRIVATE_KEY, parts[1])
    except:
        raise Exception("Invalid token")

    # role_map is a bit brute-force to make cerbos-sqlalchemy happy, but it's fine for now.
    role_map = {}
    for project in claims["projects"]:
        for role in project["roles"]:
            if role not in role_map:
                role_map[role] = []
            role_map[role].append(project["project_id"])
    return Principal(
        claims["sub"],
        roles=["user"],
        attr={
            "user_id": int(claims["sub"]),
            "admin_projects": role_map.get("admin", []),
            "member_projects": role_map.get("member", []),
        },
    )
