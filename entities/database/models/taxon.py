"""
SQLAlchemy database model for Taxon

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import TaxonLevel

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.upstream_database import UpstreamDatabase
    from database.models.consensus_genome import ConsensusGenome
    from database.models.reference_genome import ReferenceGenome
    from database.models.sequencing_read import SequencingRead
    from database.models.sample import Sample
else:
    File = "File"
    UpstreamDatabase = "UpstreamDatabase"
    ConsensusGenome = "ConsensusGenome"
    ReferenceGenome = "ReferenceGenome"
    SequencingRead = "SequencingRead"
    Sample = "Sample"


class Taxon(Entity):
    __tablename__ = "taxon"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    wikipedia_id: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    common_name: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_phage: Mapped[bool] = mapped_column(Boolean, nullable=False)
    upstream_database_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("upstream_database.entity_id"), nullable=False
    )
    upstream_database: Mapped["UpstreamDatabase"] = relationship(
        "UpstreamDatabase", back_populates="taxa", foreign_keys=upstream_database_id
    )
    upstream_database_identifier: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[TaxonLevel] = mapped_column(Enum(TaxonLevel, native_enum=False), nullable=False)
    tax_parent_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_parent: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_parent_id)
    tax_subspecies_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_subspecies: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_subspecies_id)
    tax_species_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_species: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_species_id)
    tax_genus_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_genus: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_genus_id)
    tax_family_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_family: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_family_id)
    tax_order_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_order: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_order_id)
    tax_class_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_class: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_class_id)
    tax_phylum_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_phylum: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_phylum_id)
    tax_kingdom_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_kingdom: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_kingdom_id)
    tax_superkingdom_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("taxon.entity_id"), nullable=True)
    tax_superkingdom: Mapped["Taxon"] = relationship("Taxon", foreign_keys=tax_superkingdom_id)
    consensus_genomes: Mapped[list[ConsensusGenome]] = relationship(
        "ConsensusGenome", back_populates="taxon", uselist=True, foreign_keys="ConsensusGenome.taxon_id"
    )
    reference_genomes: Mapped[list[ReferenceGenome]] = relationship(
        "ReferenceGenome", back_populates="taxon", uselist=True, foreign_keys="ReferenceGenome.taxon_id"
    )
    sequencing_reads: Mapped[list[SequencingRead]] = relationship(
        "SequencingRead", back_populates="taxon", uselist=True, foreign_keys="SequencingRead.taxon_id"
    )
    samples: Mapped[list[Sample]] = relationship(
        "Sample", back_populates="host_taxon", uselist=True, foreign_keys="Sample.host_taxon_id"
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
