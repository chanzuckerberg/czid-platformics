import uuid
import strawberry


@strawberry.type
class Entity:
    id: uuid.UUID
    type: str
    producing_run_id: uuid.UUID
    owner_user_id: int
    collection_id: int


@strawberry.interface
class EntityInterface:
    id: uuid.UUID
