"""
SQLAlchemy database model for ConsensusGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.taxon import Taxon
    from database.models.sequencing_read import SequencingRead
    from database.models.reference_genome import ReferenceGenome
    from database.models.accession import Accession
    from database.models.metric_consensus_genome import MetricConsensusGenome
else:
    File = "File"
    Taxon = "Taxon"
    SequencingRead = "SequencingRead"
    ReferenceGenome = "ReferenceGenome"
    Accession = "Accession"
    MetricConsensusGenome = "MetricConsensusGenome"


class ConsensusGenome(Entity):
    __tablename__ = "consensus_genome"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    taxon_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("taxon.entity_id"),
        nullable=False,
    )
    taxon: Mapped["Taxon"] = relationship(
        "Taxon",
        foreign_keys=taxon_id,
        back_populates="consensus_genomes",
    )
    sequence_read_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("sequencing_read.entity_id"),
        nullable=False,
    )
    sequence_read: Mapped["SequencingRead"] = relationship(
        "SequencingRead",
        foreign_keys=sequence_read_id,
        back_populates="consensus_genomes",
    )
    reference_genome_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("reference_genome.entity_id"),
        nullable=True,
    )
    reference_genome: Mapped["ReferenceGenome"] = relationship(
        "ReferenceGenome",
        foreign_keys=reference_genome_id,
        back_populates="consensus_genomes",
    )
    accession_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("accession.entity_id"),
        nullable=True,
    )
    accession: Mapped["Accession"] = relationship(
        "Accession",
        foreign_keys=accession_id,
        back_populates="consensus_genomes",
    )
    sequence_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("file.id"),
        nullable=True,
    )
    sequence: Mapped["File"] = relationship(
        "File", foreign_keys=sequence_id, cascade="all, delete-orphan", single_parent=True, post_update=True
    )
    metrics: Mapped[MetricConsensusGenome] = relationship(
        "MetricConsensusGenome",
        back_populates="consensus_genome",
        uselist=True,
        foreign_keys="MetricConsensusGenome.consensus_genome_id",
        cascade="all, delete-orphan",
    )
    intermediate_outputs_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("file.id"),
        nullable=True,
    )
    intermediate_outputs: Mapped["File"] = relationship(
        "File", foreign_keys=intermediate_outputs_id, cascade="all, delete-orphan", single_parent=True, post_update=True
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
