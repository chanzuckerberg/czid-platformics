import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.files import File
else:
    File = "File"


# Note that we use polymorphic_load=inline so that if you query db.Entity and it's a db.Sample,
# you will get the db.Sample object not lazy-loaded. Otherwise, if you try to access a field 
# of that object it will cause the error "MissingGreenlet: greenlet_spawn has not been called".

class Sample(Entity):
    __tablename__ = "sample"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}

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
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}

    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), primary_key=True)
    nucleotide: Mapped[str] = mapped_column(String, nullable=False)
    sequence: Mapped[str] = mapped_column(String, nullable=False)
    protocol: Mapped[str] = mapped_column(String, nullable=False)
    sequence_file_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("file.id"), nullable=True)
    sequence_file: Mapped[File] = relationship(File, foreign_keys=sequence_file_id)

    sample_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sample.entity_id"), nullable=False)
    sample: Mapped[Sample] = relationship(Sample, back_populates="sequencing_reads", foreign_keys=sample_id)

    contigs: Mapped[list["Contig"]] = relationship(
        "Contig",
        back_populates="sequencing_read",
        foreign_keys="Contig.sequencing_read_id",
    )


class Contig(Entity):
    __tablename__ = "contig"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}

    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), primary_key=True)
    sequence: Mapped[str] = mapped_column(String, nullable=False)

    sequencing_read_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("sequencing_read.entity_id"), nullable=False)
    sequencing_read: Mapped[Sample] = relationship(
        SequencingRead, back_populates="contigs", foreign_keys=sequencing_read_id
    )
