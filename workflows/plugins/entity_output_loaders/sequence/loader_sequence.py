"""
Sequence loader plugin
"""
from typing import List, TypedDict
from plugins.plugin_types import EntityOutputLoader
from entity_interface import EntityReference, Sample, SequencingRead


class Input(TypedDict):
    nucleotide: str
    sequence: str
    protocol: str


class SequenceLoader(EntityOutputLoader):
    async def load(self, args: Input) -> List[SequencingRead]:
        # TODO don't hardcode me :(
        sample = Sample("dummy", "Venus")
        return [SequencingRead(args["protocol"], args["sequence"], args["nucleotide"], EntityReference(entity=sample))]
