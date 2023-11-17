from typing import List, TypedDict
from plugins.plugin_types import EntityInputLoader
from entity_interface import SequencingRead


class Input(TypedDict):
    name: str
    sequencing_read: str


class FastaLoader(EntityInputLoader):
    async def load(self, args: Input) -> List[List[SequencingRead]]:
        return [
            [
                SequencingRead(
                    nucleotide=args["name"], sequence=args["sequencing_read"], protocol="my_protocol", sample=None
                )
            ]
        ]
