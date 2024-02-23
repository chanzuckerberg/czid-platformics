"""
SQLAlchemy database model for Metadatum

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
    from database.models.sample import Sample
else:
    File = "File"
    Sample = "Sample"


class Metadatum(Entity):
    __tablename__ = "metadatum"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    sample_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("sample.entity_id"),
        nullable=False,
        index=True,
    )
    sample: Mapped["Sample"] = relationship(
        "Sample",
        foreign_keys=sample_id,
        back_populates="metadatas",
    )
    field_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    value: Mapped[str] = mapped_column(String, nullable=False, index=True)
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
