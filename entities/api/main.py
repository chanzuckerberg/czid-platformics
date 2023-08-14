import typing

import database.models as db
import strawberry
import uvicorn
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, ResourceDesc
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter
from thirdparty.cerbos_sqlalchemy.query import get_query
from thirdparty.strawberry_sqlalchemy_mapper import (
    StrawberrySQLAlchemyMapper,
)
from api.core.gql_loaders import EntityLoader

from api.core.deps import get_auth_principal, get_cerbos_client, get_db_session
from api.core.settings import APISettings
from api.core.strawberry_extensions import DependencyExtension

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


async def get_base_entities(
    model: db.Entity,
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    filters: typing.List[typing.Any] = [],
):
    rd = ResourceDesc(model.__tablename__)
    plan = cerbos_client.plan_resources("view", principal, rd)
    query = get_query(
        plan,
        model,
        {
            "request.resource.attr.owner_user_id": model.owner_user_id,
            "request.resource.attr.collection_id": model.collection_id,
        },
        [],
    )
    if filters:
        query = query.filter(*filters)
    result = await session.execute(query)
    return result.scalars().all()


@strawberry.type
class Query:
    @strawberry.field(extensions=[DependencyExtension()])
    async def samples(
        id: typing.Optional[strawberry.ID] = None,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(get_auth_principal),
    ) -> typing.List[Sample]:
        filters = []
        if id:
            filters.append(db.Sample.entity_id == int(id))
        return await get_base_entities(
            db.Sample, session, cerbos_client, principal, filters
        )

    @strawberry.field(extensions=[DependencyExtension()])
    async def sequencing_reads(
        id: typing.Optional[strawberry.ID] = None,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        principal: Principal = Depends(get_auth_principal),
    ) -> typing.List[SequencingRead]:
        filters = []
        if id:
            filters.append(db.SequencingRead.entity_id == int(id))
        return await get_base_entities(
            db.SequencingRead, session, cerbos_client, principal, filters
        )


def get_context(
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(get_auth_principal),
):
    return {
        "sqlalchemy_loader": EntityLoader(
            bind=session, cerbos_client=cerbos_client, principal=principal
        ),
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
    graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
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
