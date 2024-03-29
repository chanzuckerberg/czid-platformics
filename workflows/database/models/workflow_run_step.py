"""
SQLAlchemy database model for WorkflowRunStep

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
import datetime
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from support.enums import WorkflowRunStepStatus

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.workflow_run import WorkflowRun
else:
    File = "File"
    WorkflowRun = "WorkflowRun"


class WorkflowRunStep(Entity):
    __tablename__ = "workflow_run_step"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    workflow_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("workflow_run.entity_id"),
        nullable=True,
        index=True,
    )
    workflow_run: Mapped["WorkflowRun"] = relationship(
        "WorkflowRun",
        foreign_keys=workflow_run_id,
        back_populates="steps",
    )
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[WorkflowRunStepStatus] = mapped_column(Enum(WorkflowRunStepStatus, native_enum=False), nullable=True)
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
