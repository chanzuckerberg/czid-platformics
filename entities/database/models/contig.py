import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String, Float, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.files import File
else:
    File = "File"


class Contig(Entity):
    __tablename__ = "contig"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    sequencing_read_id: Mapped[str] = mapped_column(String, nullable=False)
    sequence: Mapped[str] = mapped_column(String, nullable=False)