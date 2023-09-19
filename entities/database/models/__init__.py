# isort: skip_file
from sqlalchemy.orm import configure_mappers

from platformics.database.models.base import Base, meta, Entity  # noqa: F401
from database.models.samples import Sample, SequencingRead, Contig  # noqa: F401
from database.models.files import File, FileStatus  # noqa: F401

configure_mappers()
