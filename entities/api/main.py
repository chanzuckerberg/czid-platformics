import typing

import uvicorn
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends, FastAPI
from platformics.api.core.deps import get_auth_principal, get_cerbos_client, get_engine
from platformics.api.core.gql_loaders import EntityLoader
from platformics.settings import APISettings
from strawberry.schema.name_converter import HasGraphQLName, NameConverter
from platformics.database.connect import AsyncDB

import strawberry
from api.queries import Query
from api.mutations import Mutation
from strawberry.schema.config import StrawberryConfig
from strawberry.fastapi import GraphQLRouter


def get_context(
    engine: AsyncDB = Depends(get_engine),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(get_auth_principal),
) -> dict[str, typing.Any]:
    return {
        "sqlalchemy_loader": EntityLoader(engine=engine, cerbos_client=cerbos_client, principal=principal),
    }


# Arg/Field names that start with _ are not camel-cased
class CustomNameConverter(NameConverter):
    def get_graphql_name(self, obj: HasGraphQLName) -> str:
        if obj.python_name.startswith("_"):
            return obj.python_name
        return super().get_graphql_name(obj)


# only needed if you have polymorphic types
# additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())
# strawberry graphql schema
# start server with strawberry server app
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=True, name_converter=CustomNameConverter()),
    # types=additional_types,
)


# Make sure tests can get their own instances of the app.
def get_app() -> FastAPI:
    settings = APISettings.model_validate({})  # Workaround for https://github.com/pydantic/pydantic/issues/3753

    # Add a global settings object to the app that we can use as a dependency
    graphql_app: GraphQLRouter = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
    _app = FastAPI(
        title=settings.SERVICE_NAME,
        debug=settings.DEBUG,
    )
    _app.include_router(graphql_app, prefix="/graphql")

    # Add a global settings object to the app that we can use as a dependency
    _app.state.entities_settings = settings

    return _app


app = get_app()

if __name__ == "__main__":
    config = uvicorn.Config("api.main:app", host="0.0.0.0", port=8008, log_level="info")
    server = uvicorn.Server(config)
    server.run()
