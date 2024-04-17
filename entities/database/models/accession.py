"""
SQLAlchemy database model for Accession

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""

import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.upstream_database import UpstreamDatabase
    from database.models.consensus_genome import ConsensusGenome
else:
    File = "File"
    UpstreamDatabase = "UpstreamDatabase"
    ConsensusGenome = "ConsensusGenome"


class Accession(Entity):
    __tablename__ = "accession"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    accession_id: Mapped[str] = mapped_column(String, nullable=False)
    accession_name: Mapped[str] = mapped_column(String, nullable=False)
    upstream_database_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("upstream_database.entity_id"),
        nullable=False,
        index=True,
    )
    upstream_database: Mapped["UpstreamDatabase"] = relationship(
        "UpstreamDatabase",
        foreign_keys=upstream_database_id,
        back_populates="accessions",
    )
    consensus_genomes: Mapped[list[ConsensusGenome]] = relationship(
        "ConsensusGenome",
        back_populates="accession",
        uselist=True,
        foreign_keys="ConsensusGenome.accession_id",
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
