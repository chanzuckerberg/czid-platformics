import asyncio
import configparser
import json
import os
import typing
import asyncio

import sqlalchemy as sa
import strawberry
from fastapi import FastAPI
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from strawberry.fastapi import GraphQLRouter
from strawberry_sqlalchemy_mapper import (StrawberrySQLAlchemyLoader,
                                          StrawberrySQLAlchemyMapper)

import database.models as db
import entity_gql_schema as entity_schema
from database.connect import init_async_db
from config import load_event_buses, load_workflow_runners

from strawberry_sqlalchemy_mapper import (
    StrawberrySQLAlchemyMapper, StrawberrySQLAlchemyLoader)

from loader import LoaderDriver


############
# Database #
############
app_db = init_async_db()
session = app_db.session()

###########
# Plugins #
###########

config = configparser.ConfigParser()
config.read("defaults.cfg")
default_workflow_runner_name = config.get("plugins", "default_workflow_runner")

workflow_runners = load_workflow_runners()
event_buses = load_event_buses()

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

@strawberry_sqlalchemy_mapper.type(db.RunEntityInput)
class RunEntityInput:
    pass


@strawberry.type
class WorkflowRunner:
    name: str
    supported_workflow_types: typing.List[str]
    description: str


@strawberry.type
class Query:
    @strawberry.field
    async def get_workflow(self, id: int) -> Workflow:
        result = await session.execute(sa.select(db.Workflow).where(db.Workflow.id == id))
        return result.scalars().one()

    @strawberry.field
    async def get_workflows(self) -> typing.Sequence[Workflow]:
        result = await session.execute(sa.select(db.Workflow))
        return result.scalars().all()

    @strawberry.field
    async def get_workflow_version(self) -> WorkflowVersion:
        result = await session.execute(sa.select(db.WorkflowVersion).where(db.WorkflowVersion.id == id))
        return result.scalars().one()

    @strawberry.field
    async def get_workflow_versions(self) -> typing.Sequence[WorkflowVersion]:
        result = await session.execute(sa.select(db.WorkflowVersion))
        return result.scalars().all()
    
    @strawberry.field
    async def get_run(self) -> Run:
        result = await session.execute(sa.select(db.Run).where(db.Run.id == id))
        return result.scalars().one()

    @strawberry.field
    async def get_runs(self) -> typing.Sequence[Run]:
        result = await session.execute(sa.select(db.Run))
        return result.scalars().all()
    
    @strawberry.field
    async def get_run_step(self) -> RunStep:
        result = await session.execute(sa.select(db.RunStep).where(db.RunStep.id == id))
        return result.scalars().one()

    @strawberry.field
    async def get_run_steps(self) -> typing.Sequence[RunStep]:
        result = await session.execute(sa.select(db.RunStep))
        return result.scalars().all()
    
    @strawberry.field
    async def get_run_entity_input(self) -> RunEntityInput:
        result = await session.execute(sa.select(db.RunEntityInput).where(db.RunEntityInput.id == id))
        return result.scalars().one()

    @strawberry.field
    async def get_run_entity_inputs(self) -> typing.Sequence[RunEntityInput]:
        result = await session.execute(sa.select(db.RunEntityInput))
        return result.scalars().all()

    @strawberry.field
    async def get_workflow_runners(self) -> typing.List[WorkflowRunner]:
        return [
            WorkflowRunner(
                name=runner_name,
                supported_workflow_types=runner.supported_workflow_types(),
                description=runner.description(),
            )
            for runner_name, runner in workflow_runners.items()
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def test_connection(self) -> str:
        entity_service_url = os.getenv("ENTITY_SERVICE_URL")
        entity_service_auth_token = os.getenv("ENTITY_SERVICE_AUTH_TOKEN")
        headers = {"Authorization": f"Bearer {entity_service_auth_token}"}
        endpoint = HTTPEndpoint(entity_service_url)

        # Create query to list all samples
        op = Operation(entity_schema.Query)
        samples = op.samples()
        samples.id()
        samples.name()
        samples.location()
        data = endpoint(op, extra_headers=headers)
        print(json.dumps(data["data"]["samples"], indent=4))

        # Create a sample
        op = Operation(entity_schema.Mutation)
        op.create_sample(name="test", location="test", collection_id=444)
        data = endpoint(op, extra_headers=headers)
        print(json.dumps(data, indent=4))

        return "Hello World"

    @strawberry.mutation
    async def add_workflow(self, name: str, default_version: str, minimum_supported_version: str) -> Workflow:
        db_workflow = db.Workflow(
            name=name, default_version=default_version, minimum_supported_version=minimum_supported_version
        )
        session.add(db_workflow)
        await session.commit()
        return db_workflow

    @strawberry.mutation
    async def add_workflow_version(
        self, workflow_id: int, version: str, type: str, package_uri: str, beta: bool, deprecated: bool, graph_json: str
    ) -> WorkflowVersion:
        db_workflow_version = db.WorkflowVersion(
            workflow_id=workflow_id,
            version=version,
            type=type,
            package_uri=package_uri,
            beta=beta,
            deprecated=deprecated,
            graph_json=graph_json,
        )
        session.add(db_workflow_version)
        await session.commit()
        return db_workflow_version

    @strawberry.mutation
    async def add_run(
        self,
        user_id: int,
        project_id: int,
        execution_id: str,
        inputs_json: str,
        outputs_json: str,
        status: str,
        workflow_version_id: int,
    ) -> Run:
        db_run = db.Run(
            user_id=user_id,
            project_id=project_id,
            execution_id=execution_id,
            inputs_json=inputs_json,
            outputs_json=outputs_json,
            status=status,
            workflow_version_id=workflow_version_id,
        )
        session.add(db_run)
        await session.commit()
        return db_run

    @strawberry.mutation
    async def submit_workflow(self, workflow_inputs: str, workflow_runner: str = default_workflow_runner_name) -> str:
        # TODO: create a workflow run
        # TODO: how do we determine the docker_image_id? Argument to miniwdl, may not be defined, other devs may want to submit custom containers
        # inputs_json = {
        #     "query_0": "s3://idseq-samples-development/rlim-test/test-upload/valid_input1.fastq",
        #     "db_chunk": "s3://czid-public-references/ncbi-indexes-prod/2021-01-22/index-generation-2/nt_k14_w8_20/nt.part_001.idx",
        #     "docker_image_id": "732052188396.dkr.ecr.us-west-2.amazonaws.com/minimap2:latest"
        # }
        # inputs_json = {
        #     "sequences": "/home/todd/czid-platformics/workflows/test_workflows/foo.fa",
        # }
        assert workflow_runner in workflow_runners, f"Workflow runner {workflow_runner} not found"
        _workflow_runner = workflow_runners[workflow_runner]
        assert "WDL" in _workflow_runner.supported_workflow_types(), f"Workflow runner {workflow_runner} does not support WDL"
        response = await _workflow_runner.run_workflow(
            event_bus=event_buses["local"],
            workflow_run_id='1', # TODO: When we create the workflow run add the uuid here
            workflow_path="/home/todd/czid-platformics/workflows/test_workflows/static_sample/static_sample.wdl", # TODO: should come from the WorkflowVersion model
            inputs={}
        )
        
        return response

    @strawberry.mutation
    async def add_run_step(self, run_id: int, step_name: str, status: str, start_time: str, end_time: str) -> RunStep:
        db_run_step = db.RunStep(
            run_id=run_id, step_name=step_name, status=status, start_time=start_time, end_time=end_time
        )
        session.add(db_run_step)
        await session.commit()
        return db_run_step

    @strawberry.mutation
    async def add_run_entity_input(self, run_id: int, workflow_version_input_id: int, entity_id: int) -> RunEntityInput:
        db_run_entity_input = db.RunEntityInput(
            run_id=run_id, workflow_version_input_id=workflow_version_input_id, entity_id=entity_id
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

loader = LoaderDriver(session, event_buses["local"])

# call main in it's own thread
loop = asyncio.get_event_loop()
loop.create_task(loader.main())

@app.get("/")
async def root():
    return {"message": "Hello World"}
