"""
Populate the database with mock data for local development
"""

from database.models.workflow import Workflow
from database.models.workflow_version import WorkflowVersion

from platformics.util.seed_utils import SeedSession, DEFAULT_WORKFLOW_VERSIONS, TempCZIDWorkflowFile


def main() -> str:
    """
    An idempotent seed script to create the minimum viable set of entities to run consensus genomes

    It also creates entity and raw inputs to run the consensus genome workflow
    """
    session = SeedSession()

    version = DEFAULT_WORKFLOW_VERSIONS["consensus-genome"]
    cg_workflow = session.create_or_fetch_entity(Workflow, name="consensus-genome")
    cg_workflow.default_version = version
    cg_workflow.minimum_supported_version = version
    session.add(cg_workflow)
    session.commit()

    workflow_uri = session.transfer_wdl("run.wdl", "consensus-genome")
    cg_workflow_version = session.create_or_fetch_entity(WorkflowVersion, version=version, workflow=cg_workflow)
    cg_workflow_version.workflow_uri = workflow_uri
    with TempCZIDWorkflowFile("manifest.yml", "consensus-genome", branch="tmorse-cg-manifest") as manifest_file:
        cg_workflow_version.manifest = manifest_file.read().decode()
    cg_workflow_version.workflow = cg_workflow
    session.add(cg_workflow_version)
    session.commit()
    return str(cg_workflow_version.entity_id)


if __name__ == "__main__":
    print("Seeding database")
    version_id = main()
    print("workflow version id", version_id)
    print("Seeding complete")
