import uuid
import uuid6
from platformics.database.models.base import Base, Entity
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, Mapper, relationship
from sqlalchemy.engine import Connection
from support.enums import FileStatus, FileAccessProtocol, FileUploadClient


class File(Base):
    __tablename__ = "file"

    id: Column[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7)

    # TODO - the relationship between Entities and Files is currently being
    # configured in both directions: entities have {fieldname}_file_id fields,
    # *and* files have {entity_id, field_name} fields to map back to
    # entities. We'll probably deprecate one side of this relationship in
    # the future, but I'm not sure yet which one is going to prove to be
    # more useful.
    entity_id = mapped_column(ForeignKey("entity.id"))
    entity_field_name: Mapped[str] = mapped_column(String, nullable=False)
    entity: Mapped[Entity] = relationship(Entity, foreign_keys=entity_id)

    status: Mapped[FileStatus] = mapped_column(Enum(FileStatus, native_enum=False), nullable=False)
    protocol: Mapped[FileAccessProtocol] = mapped_column(Enum(FileAccessProtocol, native_enum=False), nullable=False)
    namespace: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    file_format: Mapped[str] = mapped_column(String, nullable=False)
    compression_type: Mapped[str] = mapped_column(String, nullable=True)
    size: Mapped[int] = mapped_column(Integer, nullable=True)
    upload_client: Mapped[FileUploadClient] = mapped_column(Enum(FileUploadClient, native_enum=False), nullable=True)
    upload_error: Mapped[str] = mapped_column(String, nullable=True)


@event.listens_for(File, "before_delete")
def before_delete(mapper: Mapper, connection: Connection, target: File) -> None:
    """
    Before deleting a File object, make sure to scrub the foreign keys in the Entity it's associated with.
    """
    table_entity = target.entity.__table__
    values = {f"{target.entity_field_name}_id": None}

    # Modifying the target.entity directly does not save changes, we need to use `connection`
    connection.execute(
        table_entity.update().where(table_entity.c.entity_id == target.entity_id).values(**values)  # type: ignore
    )
