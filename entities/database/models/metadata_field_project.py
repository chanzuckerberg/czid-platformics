# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.

import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.metadata_field import MetadataField
else:
    File = "File"
    MetadataField = "MetadataField"


class MetadataFieldProject(Entity):
    __tablename__ = "metadata_field_project"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    metadata_field_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("metadata_field.entity_id"), nullable=False)
    metadata_field: Mapped[MetadataField] = relationship(
        MetadataField, back_populates="field_group", foreign_keys=metadata_field_id
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
