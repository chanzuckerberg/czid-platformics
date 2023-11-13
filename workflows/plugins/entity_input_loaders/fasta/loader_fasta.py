from typing import List, TypedDict
from uuid import UUID
from plugin_types import EntityInputLoader
from entity_interface import EntityReference, SequencingRead


class Input(TypedDict):
    name: str
    sequencing_read: str


class FastaLoader(EntityInputLoader):
    async def load(self, args: Input) -> List[List[SequencingRead]]:
        return [
            [
                SequencingRead(
                    nucleotide=args["name"], sequence=args["sequencing_read"], protocol="my_protocol", sample=EntityReference(entity_id=UUID('018b86bd-5d7c-751d-94d2-ff4dc1057924')),
                )
            ]
        ]
