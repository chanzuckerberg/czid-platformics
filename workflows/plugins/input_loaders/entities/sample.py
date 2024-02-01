import typing
from sgqlc.operation import Operation
from database.models.workflow_version import WorkflowVersion
from manifest.manifest import EntityInput
from platformics.client.entities_schema import Query, SampleWhereClause, UUIDComparators
from plugins.plugin_types import InputLoader


class SampleInputLoader(InputLoader):
    async def load(
        self,
        workflow_version: WorkflowVersion,
        entity_inputs: dict[str, EntityInput],
        raw_inputs: dict[str, typing.Any],
        requested_outputs: list[str] = [],
    ) -> dict[str, str]:
        sample = entity_inputs["sample"]
        op = Operation(Query)
        samples = op.samples(where=SampleWhereClause(id=UUIDComparators(_eq=sample.entity_id)))
        for output in requested_outputs:
            getattr(samples, output)()
        sample = self._entities_gql(op)["data"][0]
        return {output: sample[output] for output in requested_outputs}
