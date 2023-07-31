from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, Column, Integer

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)

class Base(DeclarativeBase):
    metadata = meta

class Entity(Base):
    __tablename__ = "entity"
    __mapper_args__ = {
        "polymorphic_identity": "entity",
        "polymorphic_on": "type"
    }

    # Entity ID is used..
    id: Mapped[int] = mapped_column(primary_key=True)

    # Type is what?
    type: Mapped[str]

    # Example attributes for every entity (TODO: revisit nullable columns later)
    producing_run_id = Column(Integer, nullable=True)
    owner_user_id = Column(Integer, nullable=True)
