import typing
from database.connect import AsyncDB
import database.models as db
import strawberry
import uvicorn
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from fastapi import Depends, FastAPI
from strawberry.fastapi import GraphQLRouter
from thirdparty.strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper
from api.core.gql_loaders import EntityLoader, get_base_loader
from api.core.deps import get_auth_principal, get_cerbos_client, get_engine, get_db_session, require_auth_principal
from api.core.settings import APISettings
from api.core.strawberry_extensions import DependencyExtension
from sqlalchemy.ext.asyncio import AsyncSession

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


# --------------------
# Queries
# --------------------


@strawberry.type
class Query:
    samples: typing.List[Sample] = get_base_loader(db.Sample, Sample)
    sequencing_reads: typing.List[SequencingRead] = get_base_loader(db.SequencingRead, SequencingRead)


# --------------------
# Mutations
# --------------------


# Utility function to create a new entity
async def create_entity(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    principal: Principal = Depends(require_auth_principal),
):
    async def create(entity_model, gql_type, params):
        # Save to DB
        params["owner_user_id"] = int(principal.id)
        new_entity = entity_model(**params)
        session.add(new_entity)
        await session.commit()

        # Return GQL object to client
        params = {
            **params,
            "id": new_entity.entity_id,
            "type": new_entity.type,
            "producing_run_id": new_entity.producing_run_id,
            "entity_id": new_entity.entity_id,
        }
        return gql_type(**params)

    return create


@strawberry.type
class Mutation:
    @strawberry.mutation(extensions=[DependencyExtension()])
    async def add_sample(
        self,
        name: str,
        location: str,
        collection_id: int,
        create_entity: any = Depends(create_entity),
    ) -> Sample:
        return await create_entity(db.Sample, Sample, dict(name=name, location=location, collection_id=collection_id))


# --------------------
# Initialize app
# --------------------


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
    mutation=Mutation,
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
    config = uvicorn.Config("example:app", host="0.0.0.0", port=8008, log_level="info")
    server = uvicorn.Server(config)
    server.run()
