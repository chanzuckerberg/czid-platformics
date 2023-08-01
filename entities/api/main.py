import typing
import sqlalchemy as sa
from fastapi import FastAPI
import uvicorn

import strawberry
import database.models as db
from strawberry.fastapi import GraphQLRouter
from database.connect import init_async_db

# from strawberry_sqlalchemy_mapper import strawberry_dataclass_from_model
from strawberry_sqlalchemy_mapper import (
    StrawberrySQLAlchemyMapper, StrawberrySQLAlchemyLoader)

############
# Database #
############
app_db = init_async_db()
session = app_db.session()

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
    @strawberry.field
    async def get_sample(self, id: strawberry.ID) -> Sample:
        result = await session.execute(sa.select(db.Sample).where(db.Sample.entity_id == id))
        return result.scalars()

    @strawberry.field
    async def get_all_samples(self) -> typing.List[Sample]:
        result = await session.execute(sa.select(db.Sample))
        return result.scalars()

    @strawberry.field
    async def get_sequencing_read(self, id: strawberry.ID) -> SequencingRead:
        result = await session.execute(sa.select(db.SequencingRead).where(db.SequencingRead.entity_id == id))
        return result.scalars().one()


    @strawberry.field
    async def get_all_sequencing_reads(self) -> typing.List[SequencingRead]:
        result = await session.execute(sa.select(db.SequencingRead))
        return result.scalars()

def get_context():
    global session
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


graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=True)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    config = uvicorn.Config(
        "example:app", host="0.0.0.0", port=8008, log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()

