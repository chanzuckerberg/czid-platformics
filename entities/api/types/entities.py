import uuid

import strawberry


# @strawberry_sqlalchemy_mapper.interface(db.Entity)
@strawberry.interface
class EntityInterface:
    id: uuid.UUID
