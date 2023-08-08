import typing

from database.connect import AsyncDB, init_async_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from starlette.requests import Request
from api.core.settings import APISettings
from security.token_auth import get_token_claims


async def get_settings(request: Request) -> APISettings:
    """Get the settings object from the app state"""
    return request.app.state.entities_settings

async def get_engine(settings: APISettings = Depends(get_settings)) -> typing.AsyncGenerator[AsyncDB, None]:
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

async def get_cerbos_client():
    return CerbosClient(host="http://cerbos:3592")

async def get_auth_principal(request: Request, settings: APISettings = Depends(get_settings)) -> Principal:
    auth_header = request.headers.get("authorization")
    parts = auth_header.split()
    if parts[0].lower() != "bearer":
        raise Exception("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise Exception("Token not found")
    elif len(parts) > 2:
        raise Exception("Authorization header must be Bearer token")

    claims = get_token_claims(settings.JWK_PRIVATE_KEY, parts[1])

    return Principal(
        claims["sub"],
        roles=["user"],
        attr={
            "user_id": int(claims["sub"]),
        },
    )
