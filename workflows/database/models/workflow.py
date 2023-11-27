import enum

import strawberry
from manifest.manifest import Manifest
from platformics.database.models.base import Base
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, relationship


class Workflow(Base):
    __tablename__ = "workflow"
    # TODO: replace with uuid7
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    default_version = Column(String, nullable=False)
    minimum_supported_version = Column(String, nullable=False)
    versions = relationship("WorkflowVersion", back_populates="workflow", foreign_keys="WorkflowVersion.workflow_id")


class WorkflowVersion(Base):
    __tablename__ = "workflow_version"
    # TODO: replace with uuid7
    id = Column(Integer, primary_key=True, autoincrement=True)
    graph_json = Column(String)
    workflow_id = Column(Integer, ForeignKey("workflow.id"), nullable=False)
    workflow: Mapped[Workflow] = relationship(Workflow, back_populates="versions", foreign_keys=[workflow_id])
    runs = relationship("Run", back_populates="workflow_version", foreign_keys="Run.workflow_version_id")
    workflow_definition_uri = Column(String, nullable=False)
    manifest = Column(String, nullable=False)

    _parsed_manifest = None  # Placeholder for memoized data

    @property
    def parsed_manifest(self):
        if self._parsed_manifest is None:
            self._parsed_manifest = Manifest.model_validate_json(str(self.manifest))
        return self._parsed_manifest


@strawberry.enum
class RunStatus(enum.Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class Run(Base):
    __tablename__ = "run"
    # TODO: replace with uuid7
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    project_id = Column(Integer, nullable=False)
    started_at = Column(DateTime, nullable=False, server_default=func.now())
    ended_at = Column(DateTime)
    execution_id = Column(String, nullable=False)
    # TODO: add this back in when we add JSONB to strawberry-sqlalchemy-mapper
    # inputs_json = Column(JSONB, nullable=False)
    inputs_json = Column(String, nullable=False)
    # TODO: add this back in when we add JSONB to strawberry-sqlalchemy-mapper
    # outputs_json = Column(JSONB)
    outputs_json = Column(String, nullable=True)
    status: Column = Column(Enum(RunStatus), nullable=False, default=RunStatus.STARTED, name="status")
    workflow_version_id = Column(Integer, ForeignKey("workflow_version.id"), nullable=False)
    workflow_version = relationship("WorkflowVersion", back_populates="runs", foreign_keys=[workflow_version_id])
    run_steps = relationship("RunStep", back_populates="run", foreign_keys="RunStep.run_id")
    run_entity_inputs = relationship("RunEntityInput", back_populates="run", foreign_keys="RunEntityInput.run_id")


@strawberry.enum
class RunStepStatus(enum.Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class RunStep(Base):
    __tablename__ = "run_step"
    # TODO: replace with uuid7
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, ForeignKey("run.id"), nullable=False)
    run = relationship("Run", back_populates="run_steps", foreign_keys=[run_id])
    started_at = Column(DateTime, nullable=False, server_default=func.now())
    ended_at = Column(DateTime)
    status: Column = Column(Enum(RunStepStatus), name="status")


class RunEntityInput(Base):
    __tablename__ = "run_entity_input"
    # TODO: replace with uuid7
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, ForeignKey("run.id"), nullable=False)
    run = relationship("Run", back_populates="run_entity_inputs", foreign_keys=[run_id])
    entity_id = Column(Integer, nullable=False)
    field_name = Column(String, nullable=False)
