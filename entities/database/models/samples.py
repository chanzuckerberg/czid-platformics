from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, ForeignKey, Integer, String
from database.models.base import Entity

class Sample(Entity):
    __tablename__ = "sample"
    __mapper_args__ = { "polymorphic_identity": __tablename__ }

    id = mapped_column(ForeignKey("entity.id"), primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    sequencing_reads = relationship("SequencingRead", back_populates="sample", foreign_keys="SequencingRead.id")


class SequencingRead(Entity):
    __tablename__ = "sequencing_read"
    __mapper_args__ = { "polymorphic_identity": __tablename__ }

    id = mapped_column(ForeignKey("entity.id"), primary_key=True)
    nucleotide = Column(String, nullable=False)
    sequence = Column(String, nullable=False)
    protocol = Column(String, nullable=False)

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    sample = relationship("Sample", back_populates="sequencing_reads", foreign_keys=sample_id)
