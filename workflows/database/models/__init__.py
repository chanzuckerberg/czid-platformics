"""
Make database models importable

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/database/models/__init__.py.j2 instead.
"""

# isort: skip_file

from sqlalchemy.orm import configure_mappers

from platformics.database.models.base import Base, meta, Entity  # noqa: F401
from database.models.run import Run  # noqa: F401
from database.models.workflow import Workflow  # noqa: F401
from database.models.run_step import RunStep  # noqa: F401
from database.models.run_entity_input import RunEntityInput  # noqa: F401
from database.models.workflow_version import WorkflowVersion  # noqa: F401

from database.models.file import File, FileStatus  # noqa: F401

configure_mappers()
