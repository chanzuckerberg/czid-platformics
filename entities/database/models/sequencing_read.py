# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.

import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import SequencingProtocol, SequencingTechnology, NucleicAcid

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.sample import Sample
    from database.models.taxon import Taxon
    from database.models.consensus_genome import ConsensusGenome
    from database.models.contig import Contig
else:
    File = "File"
    Sample = "Sample"
    Taxon = "Taxon"
    ConsensusGenome = "ConsensusGenome"
    Contig = "Contig"


class SequencingRead(Entity):
    __tablename__ = "sequencing_read"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    sample_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sample.entity_id"), nullable=True)
    sample: Mapped[Sample] = relationship(Sample, back_populates="sequencing_reads", foreign_keys=sample_id)
    protocol: Mapped[SequencingProtocol] = mapped_column(Enum(SequencingProtocol, native_enum=False), nullable=False)
    r1_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=False)
    r1_file: Mapped[File] = relationship(File, foreign_keys=r1_file_id)
    r2_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    r2_file: Mapped[File] = relationship(File, foreign_keys=r2_file_id)
    technology: Mapped[SequencingTechnology] = mapped_column(
        Enum(SequencingTechnology, native_enum=False), nullable=False
    )
    nucleic_acid: Mapped[NucleicAcid] = mapped_column(Enum(NucleicAcid, native_enum=False), nullable=False)
    has_ercc: Mapped[bool] = mapped_column(Boolean, nullable=False)
    taxon_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    taxon: Mapped[Taxon] = relationship(Taxon, back_populates="sequencing_reads", foreign_keys=taxon_id)
    primer_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    primer_file: Mapped[File] = relationship(File, foreign_keys=primer_file_id)
    consensus_genomes: Mapped[list[ConsensusGenome]] = relationship(
        "ConsensusGenome", back_populates="sequence_read", uselist=True, foreign_keys="ConsensusGenome.sequence_read_id"
    )
    contigs: Mapped[list[Contig]] = relationship(
        "Contig", back_populates="sequencing_read", uselist=True, foreign_keys="Contig.sequencing_read_id"
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
