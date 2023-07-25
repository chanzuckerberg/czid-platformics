"""
Example DB test
"""
import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models.base import Base
from database.models.samples import Sample


"""
Set up database session
"""
test_db = factories.postgresql_proc(port=None, dbname="test_db")

@pytest.fixture(scope="session")
def db_session(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        engine = create_engine(f"postgresql+psycopg2://{pg_user}:@{pg_host}:{pg_port}/{pg_db}")
        Base.metadata.create_all(engine)
        yield sessionmaker(bind=engine, expire_on_commit=False)

"""
Tests
"""
class TestSamples:
    def test_samples_1(self, db_session):
        with db_session() as session:
            session.add(Sample(name="Yes", location="Mountain View, CA"))
            result = session.query(Sample).filter_by(location="Mountain View, CA").first()
            assert result.name == "Yes"

    def test_samples_2(self, db_session):
        with db_session() as session:
            sample = Sample(name="No", location="Mountain View, CA")
            session.add(sample)
            result = session.query(Sample).filter_by(location="Mountain View, CA").first()
            assert result.name == "No"
