import typing

import database.models as db
import strawberry
import uvicorn
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from database.connect import AsyncDB
from fastapi import Depends, FastAPI
from strawberry.fastapi import GraphQLRouter
from thirdparty.strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper

from api.core.deps import get_auth_principal, get_cerbos_client, get_engine
from api.core.gql_loaders import EntityLoader, get_base_loader
from api.core.settings import APISettings

######################
# Strawberry-GraphQL #
######################

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()


@strawberry_sqlalchemy_mapper.interface(db.Entity)
class EntityInterface:
    pass


@strawberry_sqlalchemy_mapper.type(db.Sample)
class Sample:
    pass


@strawberry_sqlalchemy_mapper.type(db.SequencingRead)
class SequencingRead:
    pass


@strawberry.type
class Query:
    samples: typing.List[Sample] = get_base_loader(db.Sample, Sample)
    sequencing_reads: typing.List[SequencingRead] = get_base_loader(db.SequencingRead, SequencingRead)


def get_context(
    engine: AsyncDB = Depends(get_engine),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(get_auth_principal),
):
    return {
        "sqlalchemy_loader": EntityLoader(engine=engine, cerbos_client=cerbos_client, principal=principal),
    }


# call finalize() before using the schema:
# (note that models that are related to models that are in the schema
# are automatically mapped at this stage
strawberry_sqlalchemy_mapper.finalize()
# only needed if you have polymorphic types
additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())
# strawberry graphql schema
# start server with strawberry server app
schema = strawberry.Schema(
    query=Query,
    #    mutation=Mutation,
    #    extensions=extensions,
    types=additional_types,
)


# Make sure tests can get their own instances of the app.
def get_app() -> FastAPI:
    settings = APISettings()

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
