import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Float, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.files import File
    from database.models.sample import Sample
    from support.enums import Nucleotide, SequencingProtocol
else:
    File = "File"
    Sample = "Sample"
    Nucleotide = "Nucleotide"
    SequencingProtocol = "SequencingProtocol"


class SequencingRead(Entity):
    __tablename__ = "sequencing_read"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}

    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), primary_key=True)
    nucleotide: Mapped[Nucleotide] = mapped_column(Enum(Nucleotide), nullable=True)
    sequence: Mapped[str] = mapped_column(String, nullable=True)
    protocol: Mapped[SequencingProtocol] = mapped_column(Enum(SequencingProtocol), nullable=True)
    sequence_file_id: Mapped[str] = mapped_column(String, nullable=False)
            
    sample_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sample.entity_id"), nullable=False)
    sample: Mapped[Sample] = relationship(Sample, back_populates="sequencing_reads", foreign_keys=sample_id)
            