# isort: skip_file
#from sqlalchemy.orm import configure_mappers

from database.models.base import Base, meta # noqa: F401
from database.models.samples import (Sample, SequencingRead)  # noqa: F401

#configure_mappers()