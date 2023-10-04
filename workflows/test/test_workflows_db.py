from platformics.database.connect import init_sync_db
import database.models as db
from platformics.database.models.base import Base
from factoryboy import workflow_factory as wf
import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
import os


test_db = factories.postgresql_noproc(
    host=os.getenv("PLATFORMICS_DATABASE_HOST"), password=os.getenv("PLATFORMICS_DATABASE_PASSWORD")
)


def get_db_uri(protocol, db_user, db_pass, db_host, db_port, db_name):
    db_uri = f"{protocol}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return db_uri


@pytest.fixture()
def sync_db(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        db = init_sync_db(
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


def test_workflow_creation(sync_db):
    with sync_db.session() as session:
        wf.SessionStorage.set_session(session)
        wf.WorkflowFactory.create_batch(2, name="test-workflow-name")
        wf.WorkflowFactory.create_batch(2, name="test-workflow-name2")
        assert session.query(db.Workflow).filter_by(name="test-workflow-name").count() == 2


def test_run_creation(sync_db):
    with sync_db.session() as session:
        wf.SessionStorage.set_session(session)
        wf.RunFactory.create_batch(2, status=db.RunStatus["FAILED"])
        wf.RunFactory.create_batch(3, status=db.RunStatus["SUCCEEDED"])

        assert session.query(db.Run).filter_by(status=db.RunStatus["SUCCEEDED"]).count() == 3
