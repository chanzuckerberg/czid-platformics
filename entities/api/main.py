import typing

import database.models as db
import strawberry
import uvicorn
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends, FastAPI
from platformics.api.core.deps import get_auth_principal, get_cerbos_client, get_engine
from platformics.api.core.gql_loaders import (
    EntityLoader,
    get_base_creator,
    get_base_loader,
    get_base_updater,
    get_file_loader,
)
from platformics.api.core.settings import APISettings
from platformics.database.connect import AsyncDB
from platformics.thirdparty.strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper
from strawberry.fastapi import GraphQLRouter

######################
# Strawberry-GraphQL #
######################

strawberry_sqlalchemy_mapper: StrawberrySQLAlchemyMapper = StrawberrySQLAlchemyMapper()


@strawberry_sqlalchemy_mapper.interface(db.Entity)
class EntityInterface:
    pass


@strawberry_sqlalchemy_mapper.type(db.File)
class File:
    pass


@strawberry_sqlalchemy_mapper.type(db.Sample)
class Sample(EntityInterface):
    pass


@strawberry_sqlalchemy_mapper.type(db.SequencingRead)
class SequencingRead(EntityInterface):
    pass


@strawberry_sqlalchemy_mapper.type(db.Contig)
class Contig(EntityInterface):
    pass


# --------------------
# Queries
# --------------------


@strawberry.type
class Query:
    samples: typing.Sequence[Sample] = get_base_loader(db.Sample, Sample)
    sequencing_reads: typing.Sequence[SequencingRead] = get_base_loader(db.SequencingRead, SequencingRead)
    contigs: typing.Sequence[Contig] = get_base_loader(db.Contig, Contig)
    files: typing.Sequence[File] = get_file_loader(db.File, File)


# --------------------
# Mutations
# --------------------


@strawberry.type
class Mutation:
    # Create
    create_sample: Sample = get_base_creator(db.Sample, Sample)  # type: ignore
    create_sequencing_read: SequencingRead = get_base_creator(db.SequencingRead, SequencingRead)  # type: ignore
    create_contig: Contig = get_base_creator(db.Contig, Contig)  # type: ignore

    # Update
    update_sample: Sample = get_base_updater(db.Sample, Sample)  # type: ignore


# --------------------
# Initialize app
# --------------------


def get_context(
    engine: AsyncDB = Depends(get_engine),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(get_auth_principal),
) -> dict[str, typing.Any]:
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
    mutation=Mutation,
    types=additional_types,
)


# Make sure tests can get their own instances of the app.
def get_app() -> FastAPI:
    settings = APISettings.parse_obj({})  # Workaround for https://github.com/pydantic/pydantic/issues/3753

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
