import typing
import sqlalchemy as sa
from fastapi import FastAPI

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

workflow_runner = load_workflow_runner("swipe")

######################
# Strawberry-GraphQL #
######################

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()

@strawberry_sqlalchemy_mapper.type(db.Workflow)
class Workflow:
    pass

@strawberry_sqlalchemy_mapper.type(db.WorkflowVersion)
class WorkflowVersion:
    pass

@strawberry_sqlalchemy_mapper.type(db.Run)
class Run:
    pass

@strawberry_sqlalchemy_mapper.type(db.RunStep)
class RunStep:
    pass

@strawberry_sqlalchemy_mapper.type(db.WorkflowVersionInput)
class WorkflowVersionInput:
    pass

@strawberry_sqlalchemy_mapper.type(db.WorkflowVersionOutput)
class WorkflowVersionOutput:
    pass

@strawberry_sqlalchemy_mapper.type(db.RunEntityInput)
class RunEntityInput:
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

    @strawberry.field
    async def get_workflow_version(self) -> WorkflowVersion:
        result = await session.execute(sa.select(db.WorkflowVersion).where(db.WorkflowVersion.id == id))
        return result.scalars().one()
    
    @strawberry.field
    async def get_workflow_versions(self) -> typing.List[WorkflowVersion]:
        result = await session.execute(sa.select(db.WorkflowVersion))
        return result.scalars()
    
    @strawberry.field
    async def get_run(self) -> Run:
        result = await session.execute(sa.select(db.Run).where(db.Run.id == id))
        return result.scalars().one()
    
    @strawberry.field
    async def get_runs(self) -> typing.List[Run]:
        result = await session.execute(sa.select(db.Run))
        return result.scalars()
    
    @strawberry.field
    async def get_run_step(self) -> RunStep:
        result = await session.execute(sa.select(db.RunStep).where(db.RunStep.id == id))
        return result.scalars().one()
    
    @strawberry.field
    async def get_run_steps(self) -> typing.List[RunStep]:
        result = await session.execute(sa.select(db.RunStep))
        return result.scalars()
    
    @strawberry.field
    async def get_workflow_version_input(self) -> WorkflowVersionInput:
        result = await session.execute(sa.select(db.WorkflowVersionInput).where(db.WorkflowVersionInput.id == id))
        return result.scalars().one()
    
    @strawberry.field
    async def get_workflow_version_inputs(self) -> typing.List[WorkflowVersionInput]:
        result = await session.execute(sa.select(db.WorkflowVersionInput))
        return result.scalars()
    
    @strawberry.field
    async def get_workflow_version_output(self) -> WorkflowVersionOutput:
        result = await session.execute(sa.select(db.WorkflowVersionOutput).where(db.WorkflowVersionOutput.id == id))
        return result.scalars().one()
    
    @strawberry.field
    async def get_workflow_version_outputs(self) -> typing.List[WorkflowVersionOutput]:
        result = await session.execute(sa.select(db.WorkflowVersionOutput))
        return result.scalars()
    
    @strawberry.field
    async def get_run_entity_input(self) -> RunEntityInput:
        result = await session.execute(sa.select(db.RunEntityInput).where(db.RunEntityInput.id == id))
        return result.scalars().one()
    
    @strawberry.field
    async def get_run_entity_inputs(self) -> typing.List[RunEntityInput]:
        result = await session.execute(sa.select(db.RunEntityInput))
        return result.scalars()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_workflow(self, name: str, default_version: str, minimum_supported_version: str) -> Workflow:
        db_workflow = db.Workflow(
            name = name,
            default_version = default_version,
            minimum_supported_version = minimum_supported_version
        )
        session.add(db_workflow)
        await session.commit()
        return db_workflow 

    @strawberry.mutation
    async def add_workflow_version(self, workflow_id: int, version: str, type: str, package_uri: str, beta: bool, deprecated: bool, graph_json: str) -> WorkflowVersion:
        db_workflow_version = db.WorkflowVersion(
            workflow_id = workflow_id,
            version = version,
            type = type,
            package_uri = package_uri,
            beta = beta,
            deprecated = deprecated,
            graph_json = graph_json
        )
        session.add(db_workflow_version)
        await session.commit()
        return db_workflow_version
    
    @strawberry.mutation
    async def add_run(self, user_id: int, project_id: int, execution_id: str, inputs_json: str, outputs_json: str, status: str, workflow_version_id: int) -> Run:
        db_run = db.Run(
            user_id = user_id,
            project_id = project_id,
            execution_id = execution_id,
            inputs_json = inputs_json,
            outputs_json = outputs_json,
            status = status,
            workflow_version_id = workflow_version_id
        )
        session.add(db_run)
        await session.commit()
        return db_run

    @strawberry.mutation
    async def submit_workflow(self, workflow_inputs: str) -> str:
        # TODO: create a workflow run
        # TODO: how do we determine the docker_image_id? Argument to miniwdl, may not be defined, other devs may want to submit custom containers
        inputs_json = {
            "query_0": "s3://idseq-samples-development/rlim-test/test-upload/valid_input1.fastq",
            "db_chunk": "s3://czid-public-references/ncbi-indexes-prod/2021-01-22/index-generation-2/nt_k14_w8_20/nt.part_001.idx",
            "docker_image_id": "732052188396.dkr.ecr.us-west-2.amazonaws.com/minimap2:latest"
        }
        response = workflow_runner.run_workflow(
            on_complete=lambda x: print(x), # TODO: add the listener service here
            workflow_run_id=1, # TODO: When we create the workflow run add the uuid here
            workflow_path="s3://idseq-workflows/minimap2-v1.0.0/minimap2.wdl", # TODO: should come from the WorkflowVersion model
            inputs=inputs_json
            )
        
        return response

    @strawberry.mutation
    async def add_run_step(self, run_id: int, step_name: str, status: str, start_time: str, end_time: str) -> RunStep:
        db_run_step = db.RunStep(
            run_id = run_id,
            step_name = step_name,
            status = status,
            start_time = start_time,
            end_time = end_time
        )
        session.add(db_run_step)
        await session.commit()
        return db_run_step
    
    @strawberry.mutation
    async def add_workflow_version_input(self, workflow_version_id: int, name: str, type: str, description: str) -> WorkflowVersionInput:
        db_workflow_version_input = db.WorkflowVersionInput(
            workflow_version_id = workflow_version_id,
            name = name,
            type = type,
            description = description
        )
        session.add(db_workflow_version_input)
        await session.commit()
        return db_workflow_version_input
    
    @strawberry.mutation
    async def add_workflow_version_output(self, workflow_version_id: int, name: str, type: str, description: str) -> WorkflowVersionOutput:
        db_workflow_version_output = db.WorkflowVersionOutput(
            workflow_version_id = workflow_version_id,
            name = name,
            type = type,
            description = description
        )
        session.add(db_workflow_version_output)
        await session.commit()
        return db_workflow_version_output
    
    @strawberry.mutation
    async def add_run_entity_input(self, run_id: int, workflow_version_input_id: int, entity_id: int) -> RunEntityInput:
        db_run_entity_input = db.RunEntityInput(
            run_id = run_id,
            workflow_version_input_id = workflow_version_input_id,
            entity_id = entity_id
        )
        session.add(db_run_entity_input)
        await session.commit()
        return db_run_entity_input

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