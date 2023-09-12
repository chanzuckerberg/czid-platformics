from typing import List, TypedDict
from plugin_types import EntityInputLoader
from entity_interface import Sequence

class Input(TypedDict):
    name: str
    sequence: str

class FastaLoader(EntityInputLoader):
    async def load(self, args: Input) -> List[List[Sequence]]:
        return [[Sequence(args["name"], args["sequence"])]]