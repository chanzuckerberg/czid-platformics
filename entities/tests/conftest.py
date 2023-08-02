import os
import typing

import pytest
import pytest_asyncio
from api.core.deps import get_db_session
from api.main import get_app, get_context
from database.connect import (AsyncDB, SyncDB, get_db_uri, init_async_db,
                              init_sync_db)
from database.models.base import Base
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.ext.asyncio import AsyncSession

test_db = factories.postgresql_noproc(
    host=os.getenv("DB_HOST"), password=os.getenv("DB_PASS")
)


@pytest.fixture()
def sync_db(test_db) -> typing.AsyncGenerator[SyncDB, None]:
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        db: SyncDB = init_sync_db(
            get_db_uri(
                db_host=pg_host,
                db_port=pg_port,
                db_user=pg_user,
                db_pass=pg_password,
                db_name=pg_db,
            )
        )
        Base.metadata.create_all(db.engine)
        yield db


@pytest_asyncio.fixture()
async def async_db(sync_db: SyncDB, test_db) -> typing.AsyncGenerator[AsyncDB, None]:
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    db = init_async_db(
        get_db_uri(
            db_host=pg_host,
            db_port=pg_port,
            db_user=pg_user,
            db_pass=pg_password,
            db_name=pg_db,
        )
    )
    yield db


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

    def patched_context():
        return {}

    api = get_app()
    api.dependency_overrides[get_db_session] = patched_session
    api.dependency_overrides[get_context] = patched_context
    return api


@pytest_asyncio.fixture()
async def http_client(api: FastAPI) -> AsyncClient:
    return AsyncClient(app=api, base_url="http://test")
