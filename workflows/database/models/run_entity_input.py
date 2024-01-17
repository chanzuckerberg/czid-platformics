"""
SQLAlchemy database model for RunEntityInput

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.
"""


import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.run import Run
else:
    File = "File"
    Run = "Run"


class RunEntityInput(Entity):
    __tablename__ = "run_entity_input"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    new_entity_id: Mapped[int] = mapped_column(Integer, nullable=True)
    field_name: Mapped[str] = mapped_column(String, nullable=True)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("run.entity_id"), nullable=True)
    run: Mapped["Run"] = relationship("Run", back_populates="run_entity_inputs", foreign_keys=run_id)
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)
