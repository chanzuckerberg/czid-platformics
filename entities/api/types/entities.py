import strawberry


@strawberry.type
class Entity:
    id: strawberry.ID
    type: str
    producing_run_id: strawberry.ID
    owner_user_id: int
    collection_id: int


@strawberry.interface
class EntityInterface:
    id: strawberry.ID
