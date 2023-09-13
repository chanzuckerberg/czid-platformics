from typing import List, TypedDict
from plugin_types import EntityOutputLoader
from entity_interface import SequencingRead

class Input(TypedDict):
    id: str
    sequencing_read: str

class SequenceLoader(EntityOutputLoader):
    async def load(self, args: Input) -> List[List[SequencingRead]]:
        return [[SequencingRead(args["id"], args["sequencing_read"])]]