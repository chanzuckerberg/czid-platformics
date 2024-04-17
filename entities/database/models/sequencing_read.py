"""
SQLAlchemy database model for SequencingRead

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""

import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import SequencingProtocol, SequencingTechnology

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.sample import Sample
    from database.models.taxon import Taxon
    from database.models.genomic_range import GenomicRange
    from database.models.consensus_genome import ConsensusGenome
else:
    File = "File"
    Sample = "Sample"
    Taxon = "Taxon"
    GenomicRange = "GenomicRange"
    ConsensusGenome = "ConsensusGenome"


class SequencingRead(Entity):
    __tablename__ = "sequencing_read"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    sample_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("sample.entity_id"),
        nullable=True,
        index=True,
    )
    sample: Mapped["Sample"] = relationship(
        "Sample",
        foreign_keys=sample_id,
        back_populates="sequencing_reads",
    )
    protocol: Mapped[SequencingProtocol] = mapped_column(Enum(SequencingProtocol, native_enum=False), nullable=True)
    r1_file_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("file.id"),
        nullable=True,
        index=True,
    )
    r1_file: Mapped["File"] = relationship(
        "File", foreign_keys=r1_file_id, cascade="all, delete-orphan", single_parent=True, post_update=True
    )
    r2_file_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("file.id"),
        nullable=True,
        index=True,
    )
    r2_file: Mapped["File"] = relationship(
        "File", foreign_keys=r2_file_id, cascade="all, delete-orphan", single_parent=True, post_update=True
    )
    technology: Mapped[SequencingTechnology] = mapped_column(
        Enum(SequencingTechnology, native_enum=False), nullable=False
    )
    clearlabs_export: Mapped[bool] = mapped_column(Boolean, nullable=False)
    medaka_model: Mapped[str] = mapped_column(String, nullable=True)
    taxon_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("taxon.entity_id"),
        nullable=True,
        index=True,
    )
    taxon: Mapped["Taxon"] = relationship(
        "Taxon",
        foreign_keys=taxon_id,
        back_populates="sequencing_reads",
    )
    primer_file_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("genomic_range.entity_id"),
        nullable=True,
        index=True,
    )
    primer_file: Mapped["GenomicRange"] = relationship(
        "GenomicRange",
        foreign_keys=primer_file_id,
        back_populates="sequencing_reads",
    )
    consensus_genomes: Mapped[list[ConsensusGenome]] = relationship(
        "ConsensusGenome",
        back_populates="sequencing_read",
        uselist=True,
        foreign_keys="ConsensusGenome.sequencing_read_id",
        cascade="all, delete-orphan",
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
