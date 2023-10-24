import os
import typing

import pytest
import pytest_asyncio
from platformics.database.connect import AsyncDB, SyncDB, init_async_db, init_sync_db
from platformics.database.models.base import Base
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from pytest_postgresql.executor_noop import NoopExecutor


test_db: NoopExecutor = factories.postgresql_noproc(
    host=os.getenv("PLATFORMICS_DATABASE_HOST"), password=os.getenv("PLATFORMICS_DATABASE_PASSWORD")
)  # type: ignore


def get_db_uri(
    protocol: typing.Optional[str],
    db_user: typing.Optional[str],
    db_pass: typing.Optional[str],
    db_host: typing.Optional[str],
    db_port: typing.Optional[int],
    db_name: typing.Optional[str],
) -> str:
    db_uri = f"{protocol}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return db_uri


@pytest.fixture()
def sync_db(test_db: NoopExecutor) -> typing.Generator[SyncDB, None, None]:
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        db: SyncDB = init_sync_db(
            get_db_uri(
                "postgresql+psycopg",
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
async def async_db(sync_db: SyncDB, test_db: NoopExecutor) -> typing.AsyncGenerator[AsyncDB, None]:
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    db = init_async_db(
        get_db_uri(
            "postgresql+asyncpg",  # "postgresql+asyncpg
            db_host=pg_host,
            db_port=pg_port,
            db_user=pg_user,
            db_pass=pg_password,
            db_name=pg_db,
        )
    )
    yield db
