"""
SQLAlchemy database model for IndexFile

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import IndexTypes

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.upstream_database import UpstreamDatabase
    from database.models.host_organism import HostOrganism
else:
    File = "File"
    UpstreamDatabase = "UpstreamDatabase"
    HostOrganism = "HostOrganism"


class IndexFile(Entity):
    __tablename__ = "index_file"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    name: Mapped[IndexTypes] = mapped_column(Enum(IndexTypes, native_enum=False), nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("file.id"),
        nullable=True,
        index=True,
    )
    file: Mapped["File"] = relationship(
        "File", foreign_keys=file_id, cascade="all, delete-orphan", single_parent=True, post_update=True
    )
    upstream_database_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("upstream_database.entity_id"),
        nullable=True,
        index=True,
    )
    upstream_database: Mapped["UpstreamDatabase"] = relationship(
        "UpstreamDatabase",
        foreign_keys=upstream_database_id,
        back_populates="indexes",
    )
    host_organism_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("host_organism.entity_id"),
        nullable=True,
        index=True,
    )
    host_organism: Mapped["HostOrganism"] = relationship(
        "HostOrganism",
        foreign_keys=host_organism_id,
        back_populates="indexes",
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
