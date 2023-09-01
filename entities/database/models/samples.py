from database.models.base import Entity
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from database.models.files import File
else:
    File = "File"


class Sample(Entity):
    __tablename__ = "sample"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)

    sequencing_reads: Mapped[list["SequencingRead"]] = relationship(
        "SequencingRead",
        back_populates="sample",
        foreign_keys="SequencingRead.sample_id",
    )


class SequencingRead(Entity):
    __tablename__ = "sequencing_read"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), primary_key=True)
    nucleotide: Mapped[str] = mapped_column(String, nullable=False)
    sequence: Mapped[str] = mapped_column(String, nullable=False)
    protocol: Mapped[str] = mapped_column(String, nullable=False)
    sequence_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    sequence_file: Mapped[File] = relationship(File, foreign_keys=sequence_file_id)

    sample_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sample.entity_id"), nullable=False)
    sample: Mapped[Sample] = relationship(Sample, back_populates="sequencing_reads", foreign_keys=sample_id)
