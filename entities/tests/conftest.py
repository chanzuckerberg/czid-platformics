import os
import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.base import Base

test_db = factories.postgresql_noproc(host=os.getenv("DB_HOST"), password=os.getenv("DB_PASS"))

@pytest.fixture(scope="session")
def postgresql(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        engine = create_engine(f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}")
        Base.metadata.create_all(engine)
        yield sessionmaker(bind=engine, expire_on_commit=False)
