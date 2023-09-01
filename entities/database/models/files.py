import uuid

import uuid6
from database.models.base import Base, Entity
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING
import enum
from sqlalchemy.dialects.postgresql import ENUM


class FileStatus(enum.Enum):
    AWAITING_UPLOAD = "AWAITING_UPLOAD"
    UPLOAD_COMPLETE = "UPLOAD_COMPLETE"
    UPLOAD_FAILURE = "UPLOAD_FAILURE"
    UPLOAD_SUCCESS = "UPLOAD_SUCCESS"


if TYPE_CHECKING:
    from database.models.samples import SequencingRead
else:
    SequencingRead = "SequencingRead"


class File(Base):
    __tablename__ = "file"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7)
    status: Mapped[FileStatus] = mapped_column(ENUM(FileStatus), nullable=False)

    # TODO - the relationship between Entities and Files is currently being
    # configured in both directions: entities have {fieldname}_file_id fields,
    # *and* files have {entity_id, field_name} fields to map back to
    # entities. We'll probably deprecate one side of this relationship in
    # the future, but I'm not sure yet which one is going to prove to be
    # more useful.
    entity_id: Mapped[int] = mapped_column(ForeignKey("entity.id"))
    entity_field_name: Mapped[str] = mapped_column(String, nullable=False)
    entity: Mapped[Entity] = relationship(Entity, foreign_keys=entity_id)

    protocol: Mapped[str] = mapped_column(String, nullable=False)
    namespace: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    file_format: Mapped[str] = mapped_column(String, nullable=False)
    compression_type: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
