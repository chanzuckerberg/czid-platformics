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
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
            
    sequencing_reads_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("TODO"), nullable=False)
    sequencing_reads: Mapped[SequencingRead] = relationship("SequencingRead", back_populates="TODO", foreign_keys=sequencing_reads_id)
            