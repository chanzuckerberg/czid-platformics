"""
SQLAlchemy database model for WorkflowVersion

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.workflow import Workflow
    from database.models.run import Run
else:
    File = "File"
    Workflow = "Workflow"
    Run = "Run"


class WorkflowVersion(Entity):
    __tablename__ = "workflow_version"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    graph_json: Mapped[str] = mapped_column(String, nullable=True)
    workflow_uri: Mapped[str] = mapped_column(String, nullable=True)
    version: Mapped[str] = mapped_column(String, nullable=True)
    manifest: Mapped[str] = mapped_column(String, nullable=True)
    workflow_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("workflow.entity_id"), nullable=True)
    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="versions", foreign_keys=workflow_id)
    runs: Mapped[list[Run]] = relationship(
        "Run", back_populates="workflow_version", uselist=True, foreign_keys="Run.workflow_version_id"
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
