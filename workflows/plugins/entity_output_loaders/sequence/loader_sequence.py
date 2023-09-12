from typing import List, TypedDict
from plugin_types import EntityOutputLoader
from entity_interface import Sequence

class Input(TypedDict):
    id: str
    sequence: str

class SequenceLoader(EntityOutputLoader):
    async def load(self, args: Input) -> List[List[Sequence]]:
        return [[Sequence(args["id"], args["sequence"])]]