"""
SQLAlchemy database model for Run

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""

import uuid
import datetime
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import RunStatus

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.workflow_version import WorkflowVersion
    from database.models.run_step import RunStep
    from database.models.run_entity_input import RunEntityInput
else:
    File = "File"
    WorkflowVersion = "WorkflowVersion"
    RunStep = "RunStep"
    RunEntityInput = "RunEntityInput"


class Run(Entity):
    __tablename__ = "run"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    execution_id: Mapped[str] = mapped_column(String, nullable=True)
    outputs_json: Mapped[str] = mapped_column(String, nullable=True)
    inputs_json: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus, native_enum=False), nullable=True)
    workflow_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("workflow_version.entity_id"), nullable=True
    )
    workflow_version: Mapped[WorkflowVersion] = relationship(
        WorkflowVersion, back_populates="runs", foreign_keys=workflow_version_id
    )
    run_steps: Mapped[list[RunStep]] = relationship(
        "RunStep", back_populates="run", uselist=True, foreign_keys="RunStep.run_id"
    )
    run_entity_inputs: Mapped[list[RunEntityInput]] = relationship(
        "RunEntityInput", back_populates="run", uselist=True, foreign_keys="RunEntityInput.run_id"
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
