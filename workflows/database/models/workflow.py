from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from database.models.base import Base


class Workflow(Base):
    __tablename__ = "workflow"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    minimum_supported_version = Column(String, nullable=False)
