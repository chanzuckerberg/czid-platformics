from sgqlc.operation import Operation
from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput
from platformics.client.entities_schema import (
    IndexFileWhereClause,
    IndexTypesEnumComparators,
    Query,
    SampleWhereClause,
    SequencingReadWhereClause,
    UUIDComparators,
    StrComparators,
)
from platformics.util.types_utils import JSONValue
from plugins.plugin_types import InputLoader


class SampleInputLoader(InputLoader):
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, JSONValue],
        requested_outputs: list[str] = [],
    ) -> dict[str, JSONValue]:
        sample_input = entity_inputs["sample"]
        op = Operation(Query)
        samples = op.samples(where=SampleWhereClause(id=UUIDComparators(_eq=sample_input.entity_id)))
        for output in requested_outputs:
            getattr(samples, output)()
        resp = self._entities_gql(op)
        sample = resp["samples"][0]
        return {output: sample[output] for output in requested_outputs}


class SequencingReadInputLoader(InputLoader):
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, JSONValue],
        requested_outputs: list[str] = [],
    ) -> dict[str, JSONValue]:
        sequencing_read_input = entity_inputs["sequencing_read"]
        op = Operation(Query)
        sequencing_reads = op.sequencing_reads(
            where=SequencingReadWhereClause(id=UUIDComparators(_eq=sequencing_read_input.entity_id))
        )
        self._fetch_file(sequencing_reads.r1_file())  # type: ignore
        self._fetch_file(sequencing_reads.r2_file())  # type: ignore
        non_file_outputs = [o for o in requested_outputs if o not in ["r1_file", "r2_file"]]
        for output in non_file_outputs:
            getattr(sequencing_reads, output)()
        resp = self._entities_gql(op)
        sequencing_read = resp["sequencingReads"][0]
        sequencing_read["r1_file"] = self._uri_file(sequencing_read["r1File"])
        sequencing_read["r2_file"] = self._uri_file(sequencing_read["r2File"])
        outputs = {output: sequencing_read[output] for output in requested_outputs}
        return outputs


class IndexFileInputLoader(InputLoader):
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, JSONValue],
        requested_outputs: list[str] = [],
    ) -> dict[str, JSONValue]:
        ncbi_index_version = raw_inputs["ncbi_index_version"]
        op = Operation(Query)
        index_files = op.index_files(
            where=IndexFileWhereClause(
                name=IndexTypesEnumComparators(_in=requested_outputs),
                version=StrComparators(_eq=ncbi_index_version),
            )
        )
        index_files.name()
        self._fetch_file(index_files.file())  # type: ignore
        resp = self._entities_gql(op)
        index_files = resp["indexFiles"]
        return {index_file["name"]: self._uri_file(index_file["file"]) for index_file in index_files}
