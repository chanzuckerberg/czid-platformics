from typing import List, TypedDict
from plugin_types import EntityInputLoader
from entity_interface import SequencingRead


class Input(TypedDict):
    name: str
    sequencing_read: str


class FastaLoader(EntityInputLoader):
    async def load(self, args: Input) -> List[List[SequencingRead]]:
        return [[SequencingRead(args["name"], args["sequencing_read"])]]
