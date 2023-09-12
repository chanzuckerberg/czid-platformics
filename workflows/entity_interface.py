from dataclasses import dataclass, field
import sys
from typing import List, Literal, Optional

from semver import Version

EntityType = Literal["string", "fasta", "sequence"]

@dataclass
class Entity:
    entity_type: EntityType
    version: Optional[Version] = field(default_factory=lambda: Version(0))

class String(Entity):
    entity_type = "string"
    value: str

    def __init__(self, value: str):
        self.value = value

class Fasta(Entity):
    entity_type = "fasta"
    path: str

    def __init__(self, path: str):
        self.path = path

class Sequence(Entity):
    entity_type = "sequence"
    id: str
    sequence: str
    version = Version(1)

    def __init__(self, id: str, sequence: str):
        self.id = id
        self.sequence = sequence

async def create_entities(entities: List[List[Entity]]):
    for entity_list in entities:
        for entity in entity_list:
            if isinstance(entity, String):
                print(f"create string: {entity.value}", file=sys.stderr)
            elif isinstance(entity, Sequence):
                print(f"create sequence: {entity.id}", file=sys.stderr)