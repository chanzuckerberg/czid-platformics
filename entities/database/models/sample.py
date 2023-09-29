import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Float, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.files import File
    from database.models.sequencing_read import SequencingRead
else:
    File = "File"
    SequencingRead = "SequencingRead"


class Sample(Entity):
    __tablename__ = "sample"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}

    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
            
    sequencing_reads: Mapped[list[SequencingRead]] = relationship("SequencingRead", back_populates="sample", uselist=True)
            