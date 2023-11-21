"""
SQLAlchemy database model for CoverageViz

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


class CoverageViz(Entity):
    __tablename__ = "coverage_viz"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    accession_id: Mapped[str] = mapped_column(String, nullable=False)
    coverage_viz_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    coverage_viz_file: Mapped[File] = relationship(File, foreign_keys=coverage_viz_file_id)
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
