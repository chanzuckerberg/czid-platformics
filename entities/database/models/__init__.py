# isort: skip_file
# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/database/models/__init__.py.j2 instead.

from sqlalchemy.orm import configure_mappers

from platformics.database.models.base import Base, meta, Entity  # noqa: F401
from database.models.sample import Sample  # noqa: F401
from database.models.sequencing_read import SequencingRead  # noqa: F401
from database.models.contig import Contig  # noqa: F401
from database.models.file import File, FileStatus  # noqa: F401

configure_mappers()
