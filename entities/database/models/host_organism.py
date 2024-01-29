"""
SQLAlchemy database model for HostOrganism

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
else:
    File = "File"


class HostOrganism(Entity):
    __tablename__ = "host_organism"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    name: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    host_filtering_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    host_filtering: Mapped["File"] = relationship("File", foreign_keys=host_filtering_id)
    sequence_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    sequence: Mapped["File"] = relationship("File", foreign_keys=sequence_id)
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)