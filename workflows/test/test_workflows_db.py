"""
Tests for the workflow db
"""

from platformics.database.connect import SyncDB
from test_infra.factories.main import SessionStorage

from test_infra.factories.workflow_run import WorkflowRunFactory
from test_infra.factories.workflow import WorkflowFactory
import database.models as db
from support.enums import WorkflowRunStatus


def test_workflow_creation(sync_db: SyncDB) -> None:
    """Test creating workflows"""
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        WorkflowFactory.create_batch(2, name="test-workflow-name")
        WorkflowFactory.create_batch(2, name="test-workflow-name2")

        workflows_count = session.query(db.Workflow).filter_by(name="test-workflow-name").count()
    assert workflows_count == 2


def test_run_creation(sync_db: SyncDB) -> None:
    """Test creating runs"""
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        WorkflowRunFactory.create_batch(2, status=WorkflowRunStatus["FAILED"])
        WorkflowRunFactory.create_batch(3, status=WorkflowRunStatus["SUCCEEDED"])

        workflow_runs_count = session.query(db.WorkflowRun).filter_by(status=WorkflowRunStatus["SUCCEEDED"]).count()

    assert workflow_runs_count == 3
