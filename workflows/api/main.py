import configparser
import typing
import json

import database.models as db
import strawberry
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal
from config import load_event_bus, load_workflow_runners
from fastapi import APIRouter, Depends, FastAPI, Request
from manifest import Manifest
from platformics.api.core.deps import get_auth_principal, get_cerbos_client, get_db_session, get_engine
from settings import APISettings
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.database.connect import AsyncDB
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper

from api.core.gql_loaders import WorkflowLoader, get_base_loader
from plugin_types import EventBus

###########
# Plugins #
###########

config = configparser.ConfigParser()
config.read("defaults.cfg")
default_workflow_runner_name = config.get("plugins", "default_workflow_runner")

workflow_runners = load_workflow_runners()


def get_event_bus(request: Request) -> EventBus:
    """Get the event_bus object from the app state"""
    return request.app.state.event_bus


######################
# Strawberry-GraphQL #
######################

strawberry_sqlalchemy_mapper: StrawberrySQLAlchemyMapper = StrawberrySQLAlchemyMapper()


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


@strawberry.input
class WorkflowInput:
    name: str
    value: str


@strawberry.type
class Query:
    workflows: typing.Sequence[Workflow] = get_base_loader(db.Workflow, Workflow)
    runs: typing.Sequence[Run] = get_base_loader(db.Run, Run)
    workflow_versions: typing.Sequence[WorkflowVersion] = get_base_loader(db.WorkflowVersion, WorkflowVersion)
    run_steps: typing.Sequence[RunStep] = get_base_loader(db.RunStep, RunStep)
    run_entity_inputs: typing.Sequence[RunEntityInput] = get_base_loader(db.RunEntityInput, RunEntityInput)

    @strawberry.field(extensions=[DependencyExtension()])
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
    @strawberry.mutation(extensions=[DependencyExtension()])
    async def add_workflow(
        self,
        name: str,
        default_version: str,
        minimum_supported_version: str,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
    ) -> Workflow:
        db_workflow = db.Workflow(
            name=name, default_version=default_version, minimum_supported_version=minimum_supported_version
        )
        session.add(db_workflow)
        await session.commit()
        return db_workflow  # type: ignore

    @strawberry.mutation(extensions=[DependencyExtension()])
    async def add_workflow_version(
        self,
        workflow_id: int,
        version: str,
        type: str,
        package_uri: str,
        beta: bool,
        deprecated: bool,
        graph_json: str,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
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
        return db_workflow_version  # type: ignore

    @strawberry.mutation(extensions=[DependencyExtension()])
    async def add_run(
        self,
        project_id: int,
        workflow_version_id: int,
        workflow_inputs: typing.List[WorkflowInput],
        workflow_runner: str = default_workflow_runner_name,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
        event_bus: EventBus = Depends(get_event_bus),
    ) -> Run:
        assert workflow_runner in workflow_runners, f"Workflow runner {workflow_runner} not found"
        _workflow_runner = workflow_runners[workflow_runner]
        assert (
            "WDL" in _workflow_runner.supported_workflow_types()
        ), f"Workflow runner {workflow_runner} does not support WDL"

        workflow_version = await session.get_one(db.WorkflowVersion, workflow_version_id)
        manifest = Manifest.model_validate_json(str(workflow_version.manifest))
        inputs = {input.name: input.value for input in workflow_inputs}

        execution_id = await _workflow_runner.run_workflow(
            event_bus=event_bus,
            workflow_path=manifest.package_uri,
            inputs=inputs,
        )
        workflow_run = db.Run(
            user_id=111,
            project_id=project_id,
            execution_id=execution_id,
            inputs_json=json.dumps(inputs),
            status="STARTED",
            workflow_version_id=1,
        )
        session.add(workflow_run)
        await session.commit()

        return workflow_run  # type: ignore

    @strawberry.mutation(extensions=[DependencyExtension()])
    async def add_run_step(
        self,
        run_id: int,
        step_name: str,
        status: str,
        start_time: str,
        end_time: str,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
    ) -> RunStep:
        db_run_step = db.RunStep(
            run_id=run_id, step_name=step_name, status=status, start_time=start_time, end_time=end_time
        )
        session.add(db_run_step)
        await session.commit()
        return db_run_step  # type: ignore

    @strawberry.mutation(extensions=[DependencyExtension()])
    async def add_run_entity_input(
        self,
        run_id: int,
        workflow_version_input_id: int,
        entity_id: int,
        session: AsyncSession = Depends(get_db_session, use_cache=False),
    ) -> RunEntityInput:
        db_run_entity_input = db.RunEntityInput(
            run_id=run_id, workflow_version_input_id=workflow_version_input_id, entity_id=entity_id
        )
        session.add(db_run_entity_input)
        await session.commit()
        return db_run_entity_input  # type: ignore


def get_context(
    engine: AsyncDB = Depends(get_engine),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(get_auth_principal),
) -> dict[str, typing.Any]:
    return {
        "sqlalchemy_loader": WorkflowLoader(engine=engine, cerbos_client=cerbos_client, principal=principal),
    }


root_router = APIRouter()


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


# Make sure tests can get their own instances of the app.
def get_app() -> FastAPI:
    settings = APISettings.model_validate({})  # Workaround for https://github.com/pydantic/pydantic/issues/3753
    event_bus = load_event_bus(settings)

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

    _app = FastAPI()
    # Add a global settings object to the app that we can use as a dependency
    _app.state.entities_settings = settings
    _app.state.event_bus = event_bus

    graphql_app: GraphQLRouter = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
    _app.include_router(root_router)
    _app.include_router(graphql_app, prefix="/graphql")
    return _app


app = get_app()
