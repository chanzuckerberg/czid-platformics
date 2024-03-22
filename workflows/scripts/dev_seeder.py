import argparse
from sqlalchemy.orm import joinedload, aliased
from platformics.util.seed_utils import (
    TEST_USER_ID,
    TEST_COLLECTION_ID,
)
from platformics.database.connect import init_sync_db
from test_infra.factories.main import SessionStorage
from database.models import WorkflowRun, WorkflowVersion, Workflow
from test_infra.factories.workflow_run import WorkflowRunFactory
from settings import APISettings

# maps the message type to the status of the workflow run
# before the message is sent
message_type_prestatus_map = {"started": "PENDING", "failed": "RUNNING", "succeeded": "RUNNING"}


class DevSeeder:
    """Seed the database with mock data for local development"""

    def __init__(self, user_id: int = TEST_USER_ID, collection_id: int = TEST_COLLECTION_ID) -> None:
        self.user_id = user_id
        self.collection_id = collection_id

        # set up the database session
        settings = APISettings.model_validate({})
        app_db = init_sync_db(settings.SYNC_DB_URI)
        self.sess = app_db.session()
        SessionStorage.set_session(self.sess)  # needed for seed functions

    def seed_workflow_runs(self, message_type: str, runner_id: str) -> None:
        """seed workflow runs for testing loaders"""
        # check if a workflow run with the same runner_id exists
        existing_workflow_run = self.sess.query(WorkflowRun).filter(WorkflowRun.execution_id == runner_id).one_or_none()
        if existing_workflow_run:
            print(f"Workflow run with runner_id {runner_id} already exists")
        else:
            workflow_alias = aliased(Workflow)
            workflow_version = (
                self.sess.query(WorkflowVersion)
                .join(workflow_alias, WorkflowVersion.workflow)
                .options(joinedload(WorkflowVersion.workflow))
                .filter(workflow_alias.name == "Simple Manifest")
                .first()
            )
            workflow_run = WorkflowRunFactory.create(
                owner_user_id=self.user_id,
                collection_id=self.collection_id,
                execution_id=runner_id,
                workflow_version=workflow_version,
                status=message_type_prestatus_map[message_type],
                raw_inputs_json="{}",
                outputs_json=None,
                error_message=None,
            )

            self.sess.add(workflow_run)
            self.sess.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="create dev seed data",
    )
    parser.add_argument("--user", type=int, default=TEST_USER_ID)
    parser.add_argument("--project", type=int, default=TEST_COLLECTION_ID)
    # TODO: does nothing right now
