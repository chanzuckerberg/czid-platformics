"""
Launch the GraphQL server.
"""

import typing

import uvicorn
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends, FastAPI
from platformics.api.core.deps import get_auth_principal, get_cerbos_client, get_engine, get_s3_client
from platformics.api.core.error_handler import HandleErrors
from platformics.api.core.gql_loaders import EntityLoader
from platformics.database.connect import AsyncDB
from platformics.settings import APISettings
from database.models.file import File

import strawberry
from api.mutations import Mutation
from api.queries import Query
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from strawberry.schema.name_converter import HasGraphQLName, NameConverter

# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------


def get_context(
    engine: AsyncDB = Depends(get_engine),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(get_auth_principal),
) -> dict[str, typing.Any]:
    """
    Defines sqlalchemy_loader, used by dataloaders
    """
    return {
        "sqlalchemy_loader": EntityLoader(engine=engine, cerbos_client=cerbos_client, principal=principal),
    }


class CustomNameConverter(NameConverter):
    """
    Arg/Field names that start with _ are not camel-cased
    """

    def get_graphql_name(self, obj: HasGraphQLName) -> str:
        if obj.python_name.startswith("_"):
            return obj.python_name
        return super().get_graphql_name(obj)


def get_app() -> FastAPI:
    """
    Make sure tests can get their own instances of the app.
    """
    settings = APISettings.model_validate({})  # Workaround for https://github.com/pydantic/pydantic/issues/3753
    File.set_settings(settings)
    File.set_s3_client(get_s3_client(settings))

    title = settings.SERVICE_NAME
    graphql_app: GraphQLRouter = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
    _app = FastAPI(title=title, debug=settings.DEBUG)
    _app.include_router(graphql_app, prefix="/graphql")
    # Add a global settings object to the app that we can use as a dependency
    _app.state.entities_settings = settings

    return _app


# ------------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------------

# Define schema and test schema
strawberry_config = StrawberryConfig(auto_camel_case=True, name_converter=CustomNameConverter())
schema = strawberry.Schema(query=Query, mutation=Mutation, config=strawberry_config, extensions=[HandleErrors()])

# Create and run app
app = get_app()

if __name__ == "__main__":
    config = uvicorn.Config("api.main:app", host="0.0.0.0", port=8009, log_level="info")
    server = uvicorn.Server(config)
    server.run()
