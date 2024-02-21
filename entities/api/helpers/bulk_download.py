"""
Define GraphQL types and helper functions for supporting GROUPBY queries.

Auto-gereanted by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/api/groupby_helpers.py.j2 instead.
"""



from typing import Any, Optional
import strawberry
import datetime
import uuid
from support.enums import BulkDownloadType

"""
Define groupby options for BulkDownload type.
These are only used in aggregate queries.
"""

@strawberry.type
class BulkDownloadGroupByOptions:
    download_type: Optional[BulkDownloadType] = None
    download_display_name: Optional[str] = None
    id: Optional[uuid.UUID] = None
    producing_run_id: Optional[uuid.UUID] = None
    owner_user_id: Optional[int] = None
    collection_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


def build_bulk_download_groupby_output(
    group_object: Optional[BulkDownloadGroupByOptions],
    keys: list[str],
    value: Any,
) -> BulkDownloadGroupByOptions:
    """
    Given a list of (potentially nested) fields representing the key of a groupby query and the value,
    build the proper groupby object.
    """
    if not group_object:
        group_object = BulkDownloadGroupByOptions()

    key = keys.pop(0)
    match key:
        case _:
            pass
    setattr(group_object, key, value)
    return group_object