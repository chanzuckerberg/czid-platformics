"""
SQLAlchemy database model for GenomicRange

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.reference_genome import ReferenceGenome
    from database.models.sequencing_read import SequencingRead
else:
    File = "File"
    ReferenceGenome = "ReferenceGenome"
    SequencingRead = "SequencingRead"


class GenomicRange(Entity):
    __tablename__ = "genomic_range"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    reference_genome_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("reference_genome.entity_id"), nullable=False
    )
    reference_genome: Mapped["ReferenceGenome"] = relationship(
        "ReferenceGenome", back_populates="genomic_ranges", foreign_keys=reference_genome_id
    )
    file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    file: Mapped["File"] = relationship("File", foreign_keys=file_id)
    sequencing_reads: Mapped[list[SequencingRead]] = relationship(
        "SequencingRead", back_populates="primer_file", uselist=True, foreign_keys="SequencingRead.primer_file_id"
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
