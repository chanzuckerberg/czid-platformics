from database.models.base import Entity
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


class Sample(Entity):
    __tablename__ = "sample"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    entity_id = mapped_column(ForeignKey("entity.id"), primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    sequencing_reads: Mapped[list["SequencingRead"]] = relationship(
        "SequencingRead",
        back_populates="sample",
        foreign_keys="SequencingRead.sample_id",
    )


class SequencingRead(Entity):
    __tablename__ = "sequencing_read"
    __mapper_args__ = {"polymorphic_identity": __tablename__}

    entity_id = mapped_column(ForeignKey("entity.id"), primary_key=True)
    nucleotide = Column(String, nullable=False)
    sequence = Column(String, nullable=False)
    protocol = Column(String, nullable=False)

    sample_id = Column(UUID, ForeignKey("sample.entity_id"), nullable=False)
    sample: Mapped[Sample] = relationship("Sample", back_populates="sequencing_reads", foreign_keys=sample_id)
