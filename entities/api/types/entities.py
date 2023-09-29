import typing

import database.models as db
import uvicorn
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends, FastAPI
from platformics.api.core.deps import (get_auth_principal, get_cerbos_client,
                                       get_engine)
from platformics.api.core.gql_loaders import (EntityLoader, get_base_creator,
                                              get_base_loader,
                                              get_base_updater,
                                              get_file_loader)
from platformics.api.core.settings import APISettings
from platformics.database.connect import AsyncDB

import strawberry
from api.files import File, SignedURL, create_file, mark_upload_complete
from api.strawberry import strawberry_sqlalchemy_mapper
from strawberry.fastapi import GraphQLRouter

@strawberry_sqlalchemy_mapper.interface(db.Entity)
class EntityInterface:
    pass
