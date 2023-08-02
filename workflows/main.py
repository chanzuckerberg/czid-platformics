import typing
import json
import sqlalchemy as sa
from fastapi import FastAPI
import uvicorn

import strawberry
from strawberry.fastapi import GraphQLRouter

import database.models as db
from database.connect import init_async_db
from config import load_workflow_runner

from strawberry_sqlalchemy_mapper import (
    StrawberrySQLAlchemyMapper, StrawberrySQLAlchemyLoader)


############
# Database #
############
app_db = init_async_db()
session = app_db.session()

###########
# Plugins #
###########

workflow_runner = load_workflow_runner("local")

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

    @strawberry.mutation
    async def submit_workflow(self, workflow_inputs: str) -> str:
        def runner(inputs_json):
            workflow_runner.run_workflow(on_complete=lambda x: print(x), workflow_run_id=1, workflow_path="/workflows/test_workflows/minimap2.wdl", inputs=inputs_json)
        inputs_json = json.loads(workflow_inputs)
        import pdb; pdb.set_trace()
        runner(inputs_json)
        
        return "{success: true}"

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