from database.models.workflow_run import WorkflowRun
from sgqlc.operation import Operation
from manifest.manifest import EntityInput, Primitive
from platformics.client.entities_schema import (
    BulkDownloadCreateInput,
    BulkDownloadType,
    FileCreate,
    ID,
    Mutation,
)
from platformics.util.types_utils import JSONValue
from plugins.plugin_types import OutputLoader


class BulkDownloadOutputLoader(OutputLoader):
    async def load(
        self,
        workflow_run: WorkflowRun,
        entity_inputs: dict[str, EntityInput | list[EntityInput]],
        raw_inputs: dict[str, Primitive | list[Primitive]],
        workflow_outputs: dict[str, JSONValue],
    ) -> None:
        op = Operation(Mutation)

        download_type = raw_inputs["bulk_download_type"]
        assert isinstance(download_type, str)

        file_path = workflow_outputs["file"]
        assert isinstance(file_path, str)

        bulk_download = op.create_bulk_download(
            input=BulkDownloadCreateInput(
                producing_run_id=ID(workflow_run.id),
                collection_id=int(workflow_run.collection_id),
                download_type=BulkDownloadType(download_type),
            )
        )
        bulk_download.id()
        res = self._entities_gql(op)

        op = Operation(Mutation)
        bulk_download_id = res["createBulkDownload"]["id"]
        file = op.create_file(
            entity_id=bulk_download_id,
            entity_field_name="file",
            file=FileCreate(name="file", file_format="fasta", **self._parse_uri(file_path)),
        )
        file.id()
        self._entities_gql(op)
