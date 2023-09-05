from typing import List


class Entity:
    pass

class String(Entity):
    value: str

    def __init__(self, value: str):
        self.value = value


class Sequence(Entity):
    value: str

    def __init__(self, value: str):
        self.value = value

async def create_entities(entities: List[Entity]):
    for entity in entities:
        if isinstance(entity, String):
            print(f"create string: {entity.value}")
        elif isinstance(entity, Sequence):
            print(f"create sequence: {entity.value}")