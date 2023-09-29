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
    nucleotide: Mapped[Nucleotide] = mapped_column(Enum(Nucleotide), nullable=False)
    sequence: Mapped[str] = mapped_column(String, nullable=False)
    protocol: Mapped[SequencingProtocol] = mapped_column(Enum(SequencingProtocol), nullable=False)
    sequence_file_id: Mapped[str] = mapped_column(String, nullable=False)
            
    sample_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("TODO"), nullable=False)
    sample: Mapped[Sample] = relationship("Sample", back_populates="TODO", foreign_keys=sample_id)
            