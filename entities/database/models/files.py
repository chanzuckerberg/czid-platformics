import uuid

import uuid6
from database.models.base import Base, Entity
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship


class File(Base):
    __tablename__ = "file"

    id: Column[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7)

    # TODO - the relationship between Entities and Files is currently being
    # configured in both directions: entities have {fieldname}_file_id fields,
    # *and* files have {entity_id, field_name} fields to map back to
    # entities. We'll probably deprecate one side of this relationship in
    # the future, but I'm not sure yet which one is going to prove to be
    # more useful.
    entity_id = mapped_column(ForeignKey("entity.id"))
    entity_field_name = Column(String)
    entity: Mapped[Entity] = relationship(Entity, foreign_keys=entity_id)

    status = mapped_column(String, nullable=False)
    protocol = mapped_column(String, nullable=False)
    namespace = Column(String, nullable=False)
    path = Column(String, nullable=False)
    file_format = Column(String, nullable=False)
    compression_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
