"""
SQLAlchemy database model for HostOrganism

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Integer, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import HostOrganismCategory

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.index_file import IndexFile
    from database.models.sample import Sample
else:
    File = "File"
    IndexFile = "IndexFile"
    Sample = "Sample"


class HostOrganism(Entity):
    __tablename__ = "host_organism"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    rails_host_genome_id: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[HostOrganismCategory] = mapped_column(
        Enum(HostOrganismCategory, native_enum=False), nullable=False
    )
    is_deuterostome: Mapped[bool] = mapped_column(Boolean, nullable=False)
    indexes: Mapped[list[IndexFile]] = relationship(
        "IndexFile",
        back_populates="host_organism",
        uselist=True,
        foreign_keys="IndexFile.host_organism_id",
    )
    samples: Mapped[list[Sample]] = relationship(
        "Sample",
        back_populates="host_organism",
        uselist=True,
        foreign_keys="Sample.host_organism_id",
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
