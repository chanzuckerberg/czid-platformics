"""
Test workflow_runs null
"""

import pytest
from platformics.database.connect import SyncDB
from test.conftest import GQLTestClient
from test_infra.factories.main import SessionStorage
from test_infra.factories.workflow_version import WorkflowVersionFactory
from test_infra.factories.workflow import WorkflowFactory


@pytest.fixture()
def read_manifest() -> str:
    with open("/workflows/manifest/test_manifests/simple.yaml") as f:
        manifest_str = f.read()
    return manifest_str


@pytest.mark.asyncio
async def test_null_workflow_run_fail(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
    read_manifest: str,
) -> None:
    owner_user_id = 333
    collection_id = 444

    with sync_db.session() as session:
        SessionStorage.set_session(session)
        cg_workflow = WorkflowFactory.create(
            name="consensus-genome", owner_user_id=owner_user_id, collection_id=collection_id
        )
        cg_workflow_version = WorkflowVersionFactory.create(
            workflow=cg_workflow,
            owner_user_id=owner_user_id,
            collection_id=collection_id,
            deprecated=False,
            manifest=read_manifest,
        )
        bd_workflow = WorkflowFactory.create(
            name="bulk-download", owner_user_id=owner_user_id, collection_id=collection_id
        )
        bd_workflow_version = WorkflowVersionFactory.create(
            workflow=bd_workflow,
            owner_user_id=owner_user_id,
            collection_id=collection_id,
            deprecated=False,
            manifest=read_manifest,
        )

    request = f"""
    mutation MyMutation {{
        runWorkflowVersion(
            input: {{ workflowVersionId: "{cg_workflow_version.id}", 
            entityInputs: [{{name: "consensus_genomes", entityId: "uuid", entityType: "consensus_genome"}}], 
            rawInputJson: "{{ \\"bulk_download_type\\": \
                \\"consensus_genome_intermediate_output_files\\", \
                \\"aggregate_action\\": \\"zip\\" }}"}}
        ) {{
            id
        }}
    }}
    """
    output = await gql_client.query(request, user_id=owner_user_id, member_projects=[collection_id])
    assert "Collection ID is required for this workflow" in output["errors"][0]["message"]

    output = await gql_client.query(
        request.replace(str(cg_workflow_version.id), str(bd_workflow_version.id)),
        user_id=owner_user_id,
        member_projects=[collection_id],
        owner_projects=[collection_id],
    )
    # Should still fail, but get farther
    error = (
        "Invalid input: Entity input not found: consensus_genomes"
        ", Missing required Entity input: sample, Raw input not found: bulk_download_type, "
        "Raw input not found: aggregate_action"
    )

    assert error in output["errors"][0]["message"]


@pytest.mark.asyncio
async def test_null_collection_id_workflow_entity_input(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    owner_user_id = 333
    collection_id = 444

    request = """
        mutation MyMutation2 {
            createWorkflowRunEntityInput(
                input: {fieldName: "a_field_name", entityType: "an_entity_type"}
            ) {
                id
            }
        }
    """
    output = await gql_client.query(request, user_id=owner_user_id, member_projects=[collection_id])
    assert "Unauthorized: Cannot create entity in this collection" == output["errors"][0]["message"].strip()
