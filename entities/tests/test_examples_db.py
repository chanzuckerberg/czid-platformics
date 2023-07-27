import os
from test_infra import factories as fa
import factory.random
from pytest_postgresql import factories
from database.connect import init_sync_db, get_db_uri
from database.models import Sample
from database.models.base import Base

# Create database tables
def init_db(**kwargs):
    db_uri = get_db_uri(db_name=kwargs["dbname"])
    app_db = init_sync_db(db_uri)
    Base.metadata.create_all(app_db.engine)
    with app_db.session() as session:
        fa.SessionStorage.set_session(session)
        factory.random.reseed_random(123)
        fa.SampleFactory.create_batch(2, location="San Francisco, CA")
        fa.SampleFactory.create_batch(5, location="Mountain View, CA")
postgresql_in_docker = factories.postgresql_noproc(host=os.getenv("DB_HOST"), password=os.getenv("DB_PASS"), load=[init_db])
postgresql = factories.postgresql("postgresql_in_docker")

# Tests
def test_samples(postgresql):
    app_db = init_sync_db(get_db_uri(db_name="tests"))
    with app_db.session() as session:
        assert session.query(Sample).filter_by(location="Mountain View, CA").count() == 5
