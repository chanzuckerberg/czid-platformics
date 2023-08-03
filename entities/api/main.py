import typing

import database.models as db
import sqlalchemy as sa
import strawberry
import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter
from strawberry_sqlalchemy_mapper import (StrawberrySQLAlchemyLoader,
                                          StrawberrySQLAlchemyMapper)
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource, ResourceAction, ResourceList
from fastapi import HTTPException, status

from api.core.deps import get_db_session, get_cerbos_client, get_user_info
from api.core.strawberry_extensions import DependencyExtension

######################
# Strawberry-GraphQL #
######################

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()


@strawberry_sqlalchemy_mapper.type(db.Sample)
class Sample:
    sequencing_reads: typing.List["SequencingRead"]


@strawberry_sqlalchemy_mapper.type(db.SequencingRead)
class SequencingRead:
    sample: "Sample"


@strawberry.type
class Query:
    @strawberry.field(extensions=[DependencyExtension()])
    async def get_sample(
        self,
        id: strawberry.ID,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
    ) -> Sample:
        result = await session.execute(
            sa.select(db.Sample).where(db.Sample.entity_id == id)
        )
        return result.scalars()

    @strawberry.field(extensions=[DependencyExtension()])
    async def get_all_samples(
        self,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        cerbos_client: CerbosClient = Depends(get_cerbos_client),
        user_info: Principal = Depends(get_user_info),
    ) -> typing.List[Sample]:
        resource = Resource(
            "0001",
            "sample",
            attr={
                "owner": "bugs_bunny",
                "public": False
            },
        )

        if not cerbos_client.is_allowed("view", user_info, resource):
            raise Exception("Hell no")

        result = await session.execute(sa.select(db.Sample))
        return result.scalars()

    @strawberry.field(extensions=[DependencyExtension()])
    async def get_sequencing_read(
        self,
        id: strawberry.ID,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
    ) -> SequencingRead:
        await session.execute(
            sa.select(db.SequencingRead).where(db.SequencingRead.entity_id == id)
        )

    @strawberry.field(extensions=[DependencyExtension()])
    async def get_all_sequencing_reads(
        self, session: AsyncSession = Depends(get_db_session, use_cache=False)
    ) -> typing.List[SequencingRead]:
        result = await session.execute(sa.select(db.SequencingRead))
        return result.scalars()


def get_context(session: AsyncSession = Depends(get_db_session, use_cache=False)):
    return {
        "sqlalchemy_loader": StrawberrySQLAlchemyLoader(bind=session),
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
    graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
    _app = FastAPI()
    _app.include_router(graphql_app, prefix="/graphql")
    return _app


app = get_app()

if __name__ == "__main__":
    config = uvicorn.Config("example:app", host="0.0.0.0", port=8008, log_level="info")
    server = uvicorn.Server(config)
    server.run()
