import typing
import sqlalchemy as sa
from fastapi import FastAPI
import uvicorn

import strawberry
import database.models as db
from strawberry.fastapi import GraphQLRouter
from database.connect import init_async_db
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

@strawberry_sqlalchemy_mapper.type(db.Workflow)
class Workflow:
    pass
    

@strawberry.type
class Query:
    @strawberry.field
    async def get_workflow(self, id: int ) -> Workflow:
        result = await session.execute(sa.select(db.Workflow).where(db.Workflow.id == id))
        return result.scalars().one()
    
    @strawberry.field
    async def get_workflows(self) -> typing.List[Workflow]:
        result = await session.execute(sa.select(db.Workflow))
        return result.scalars()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_workflow(self, name: str, version: str, minimum_supported_version: str) -> Workflow:
        db_workflow = db.Workflow(
            name = name,
            version = version,
            minimum_supported_version = minimum_supported_version
        )
        session.add(db_workflow)
        await session.commit()
        return db_workflow 

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
    mutation=Mutation,
#    extensions=extensions,
    types=additional_types,
)

graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=True)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Hello World"}