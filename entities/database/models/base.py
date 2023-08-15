from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy import MetaData, Column, Integer
import sqlalchemy
import uuid6
import uuid
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from typing import cast

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


PostgreSQLUUID = cast(
    "sqlalchemy.types.TypeEngine[uuid6.UUID]",
    sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
)


class Base(DeclarativeBase):
    metadata = meta


class Entity(Base):
    __tablename__ = "entity"
    __mapper_args__ = {"polymorphic_identity": "entity", "polymorphic_on": "type"}

    # id: Mapped[int] = Column(
    #    Integer,
    #    primary_key=True)
    id: Mapped[uuid.UUID] = Column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid6.uuid7
    )

    # The "type" field distinguishes between subclasses (e.g. sample, sequencing_read, etc)
    type: Mapped[str]

    # Example attributes for every entity (TODO: revisit nullable columns later)
    producing_run_id = Column(Integer, nullable=True)
    owner_user_id = Column(Integer, nullable=False)
    collection_id = Column(Integer, nullable=False)
