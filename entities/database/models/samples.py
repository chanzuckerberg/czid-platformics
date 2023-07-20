from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from database.models.base import Base

class Sample(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    sequencing_reads = relationship("SequencingRead", back_populates="sample")


class SequencingRead(Base):
    __tablename__ = "sequencing_read"
    sequencing_read_id = Column(Integer, primary_key=True, autoincrement=True)

    nucleotide = Column(String, nullable=False)
    sequence = Column(String, nullable=False)
    protocol = Column(String, nullable=False)

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)

    sample = relationship("Sample", back_populates="sequencing_reads")

