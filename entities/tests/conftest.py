import os

import pytest
from database.connect import get_db_uri
from database.models.base import Base
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

test_db = factories.postgresql_noproc(
    host=os.getenv("DB_HOST"), password=os.getenv("DB_PASS")
)


@pytest.fixture(scope="session")
def postgresql(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        engine = create_engine(
            get_db_uri(
                db_host=pg_host, db_port=pg_port, db_user=pg_user, db_pass=pg_password
            )
        )
        Base.metadata.create_all(engine)
        yield sessionmaker(bind=engine, expire_on_commit=False)
