"""
SQLAlchemy database model for MetricConsensusGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.consensus_genome import ConsensusGenome
else:
    File = "File"
    ConsensusGenome = "ConsensusGenome"


class MetricConsensusGenome(Entity):
    __tablename__ = "metric_consensus_genome"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    consensus_genome_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("consensus_genome.entity_id"), nullable=False, index=True
    )
    consensus_genome: Mapped["ConsensusGenome"] = relationship(
        "ConsensusGenome", back_populates="metrics", foreign_keys=consensus_genome_id
    )
    reference_genome_length: Mapped[int] = mapped_column(Float, nullable=True)
    percent_genome_called: Mapped[int] = mapped_column(Float, nullable=True)
    percent_identity: Mapped[int] = mapped_column(Float, nullable=True)
    gc_percent: Mapped[int] = mapped_column(Float, nullable=True)
    total_reads: Mapped[int] = mapped_column(Integer, nullable=True)
    mapped_reads: Mapped[int] = mapped_column(Integer, nullable=True)
    ref_snps: Mapped[int] = mapped_column(Integer, nullable=True)
    n_actg: Mapped[int] = mapped_column(Integer, nullable=True)
    n_missing: Mapped[int] = mapped_column(Integer, nullable=True)
    n_ambiguous: Mapped[int] = mapped_column(Integer, nullable=True)
    coverage_depth: Mapped[int] = mapped_column(Float, nullable=True)
    coverage_breadth: Mapped[int] = mapped_column(Float, nullable=True)
    coverage_bin_size: Mapped[int] = mapped_column(Float, nullable=True)
    coverage_total_length: Mapped[int] = mapped_column(Integer, nullable=True)
    coverage_viz: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
