import typing

from database.connect import AsyncDB, init_async_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal

async def get_engine() -> typing.AsyncGenerator[AsyncDB, None]:
    """Wrap resolvers in a DB engine"""
    engine = init_async_db()
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

async def get_user_info():
    return Principal(
        "bugs_bunny",
        roles=["user"],
        attr={
            "user_id": 1,
            "beta_tester": True,
        },
    )
