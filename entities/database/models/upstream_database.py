# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/database/models/class_name.py.j2 instead.

import uuid
from typing import TYPE_CHECKING

from platformics.database.models.base import Entity
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.file import File
    from database.models.taxon import Taxon
else:
    File = "File"
    Taxon = "Taxon"


class UpstreamDatabase(Entity):
    __tablename__ = "upstream_database"
    __mapper_args__ = {"polymorphic_identity": __tablename__, "polymorphic_load": "inline"}
    name: Mapped[str] = mapped_column(String, nullable=False)
    taxa: Mapped[list[Taxon]] = relationship(
        "Taxon", back_populates="upstream_database", uselist=True, foreign_keys="Taxon.upstream_database_id"
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity.id"), nullable=False, primary_key=True)