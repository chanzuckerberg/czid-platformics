"""
SQLAlchemy database model for Sample

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.host_organism import HostOrganism
    from database.models.sequencing_read import SequencingRead
    from database.models.metadatum import Metadatum
else:
    File = "File"
    HostOrganism = "HostOrganism"
    SequencingRead = "SequencingRead"
    Metadatum = "Metadatum"


class Sample(Entity):
    __tablename__ = "sample"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    rails_sample_id: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    host_organism_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("host_organism.entity_id"),
        nullable=True,
        index=True,
    )
    host_organism: Mapped["HostOrganism"] = relationship(
        "HostOrganism",
        foreign_keys=host_organism_id,
        back_populates="samples",
    )
    sequencing_reads: Mapped[list[SequencingRead]] = relationship(
        "SequencingRead",
        back_populates="sample",
        uselist=True,
        foreign_keys="SequencingRead.sample_id",
        cascade="all, delete-orphan",
    )
    metadatas: Mapped[list[Metadatum]] = relationship(
        "Metadatum",
        back_populates="sample",
        uselist=True,
        foreign_keys="Metadatum.sample_id",
        cascade="all, delete-orphan",
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
