"""
SQLAlchemy database model for ReferenceGenome

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
import datetime
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Float, Integer, Enum, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.sequencing_read import SequencingRead
else:
    File = "File"
    SequencingRead = "SequencingRead"


class ReferenceGenome(Entity):
    __tablename__ = "reference_genome"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    file: Mapped["File"] = relationship("File", foreign_keys=file_id)
    accession_id: Mapped[str] = mapped_column(String, nullable=True)
    accession_name: Mapped[str] = mapped_column(String, nullable=True)
    sequencing_reads: Mapped[list[SequencingRead]] = relationship(
        "SequencingRead",
        back_populates="reference_sequence",
        uselist=True,
        foreign_keys="SequencingRead.reference_sequence_id",
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
