import enum
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, DateTime, Enum, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import strawberry


Base = declarative_base()


class Workflow(Base):
    __tablename__ = 'workflow'
    id = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    default_version = Column(String, nullable=False)
    minimum_supported_version = Column(String)
    versions = relationship('WorkflowVersion', back_populates='workflow')


class WorkflowVersion(Base):
    __tablename__ = 'workflow_version'
    id = Column(UUID, primary_key=True, default=uuid4())
    version = Column(String, nullable=False)
    workflow_type = Column(String, nullable=False)
    package_uri = Column(String, nullable=False)
    beta = Column(String, nullable=False)
    deprecated = Column(String, nullable=False)
    # TODO: add this back in when we add JSONB to strawberry-sqlalchemy-mapper
    # graph_json = Column(JSONB)
    graph_json = Column(String)
    workflow_id = Column(UUID, ForeignKey('workflow.id'), nullable=False)
    workflow = relationship('Workflow', back_populates='versions')
    runs = relationship('Run', back_populates='workflow_version')


@strawberry.enum
class RunStatus(enum.Enum):
    STARTED = 'STARTED'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


class Run(Base):
    __tablename__ = 'run'
    id = Column(UUID, primary_key=True, default=uuid4())
    user_id = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=False, server_default=func.now())
    ended_at = Column(DateTime)
    execution_id = Column(String, nullable=False)
    # TODO: add this back in when we add JSONB to strawberry-sqlalchemy-mapper
    # inputs_json = Column(JSONB, nullable=False)
    inputs_json = Column(String, nullable=False)
    # TODO: add this back in when we add JSONB to strawberry-sqlalchemy-mapper
    # outputs_json = Column(JSONB)
    outputs_json = Column(String)
    status = Column(Enum(RunStatus), nullable=False, default=RunStatus.STARTED, name='status')
    workflow_version_id = Column(UUID, ForeignKey('workflow_version.id'), nullable=False)
    workflow_version = relationship('WorkflowVersion', back_populates='runs')