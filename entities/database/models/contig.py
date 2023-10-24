import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.files import File
    from database.models.sequencing_read import SequencingRead
else:
    File = "File"
    SequencingRead = "SequencingRead"


class Contig(Entity):
    __tablename__ = "contig"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    sequencing_read_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sequencing_read.entity_id"), nullable=True)
    sequencing_read: Mapped[SequencingRead] = relationship(
        SequencingRead, back_populates="contigs", foreign_keys=sequencing_read_id
    )
    sequence: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
