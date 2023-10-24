import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import Nucleotide, SequencingProtocol

if TYPE_CHECKING:
    from database.models.files import File
    from database.models.sample import Sample
    from database.models.contig import Contig
else:
    File = "File"
    Sample = "Sample"
    Contig = "Contig"


class SequencingRead(Entity):
    __tablename__ = "sequencing_read"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    nucleotide: Mapped[Nucleotide] = mapped_column(Enum(Nucleotide), nullable=False)
    sequence: Mapped[str] = mapped_column(String, nullable=False)
    protocol: Mapped[SequencingProtocol] = mapped_column(Enum(SequencingProtocol), nullable=False)
    sequence_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    sequence_file: Mapped[File] = relationship(File, foreign_keys=sequence_file_id)
    sample_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sample.entity_id"), nullable=True)
    sample: Mapped[Sample] = relationship(Sample, back_populates="sequencing_reads", foreign_keys=sample_id)
    contigs: Mapped[list[Contig]] = relationship(
        "Contig", back_populates="sequencing_read", uselist=True, foreign_keys="Contig.sequencing_read_id"
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
