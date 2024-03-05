"""
GraphQL web app runner
"""
from datetime import datetime
import json
import logging
import typing

import database.models as db
import strawberry
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from fastapi import APIRouter, Depends, FastAPI, Request
from manifest.manifest import EntityInput, Manifest
from platformics.api.core.deps import (
    get_auth_principal,
    get_cerbos_client,
    get_db_session,
    get_engine,
    get_user_token,
    require_auth_principal,
)
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.database.connect import AsyncDB
from plugins.plugin_types import EventBus, WorkflowRunner
from settings import APISettings
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from strawberry.schema.name_converter import HasGraphQLName, NameConverter

from api.config import load_event_bus, load_workflow_runner, resolve_input_loader
from platformics.api.core.gql_loaders import EntityLoader
from api.mutations import Mutation as CodegenMutation
from api.queries import Query
from api.types import workflow_run
from support.enums import WorkflowRunStatus

###########
# Plugins #
###########


def get_event_bus(request: Request) -> EventBus:
    """Get the event_bus object from the app state"""
    return request.app.state.event_bus


def get_workflow_runner(request: Request) -> WorkflowRunner:
    return request.app.state.workflow_runner


######################
# Strawberry-GraphQL #
######################


@strawberry.input
class WorkflowInput:
    name: str
    value: str


def get_context(
    engine: AsyncDB = Depends(get_engine),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(get_auth_principal),
) -> dict[str, typing.Any]:
    """
    Injects the sqlalchemy_loader variable into GQL queries
    """
    return {
        "sqlalchemy_loader": EntityLoader(engine=engine, cerbos_client=cerbos_client, principal=principal),
    }


root_router = APIRouter()


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


class CustomNameConverter(NameConverter):
    """
    Arg/Field names that start with _ are not camel-cased
    """

    def get_graphql_name(self, obj: HasGraphQLName) -> str:
        if obj.python_name.startswith("_"):
            return obj.python_name
        return super().get_graphql_name(obj)


@strawberry.input()
class EntityInputType:
    name: str
    entity_id: strawberry.ID
    entity_type: str


@strawberry.input()
class RunWorkflowVersionInput:
    collection_id: int
    workflow_version_id: strawberry.ID
    entity_inputs: typing.Optional[list[EntityInputType]]
    raw_input_json: typing.Optional[str]
    rails_workflow_run_id: typing.Optional[int] = None


async def _create_workflow_run(
    input: RunWorkflowVersionInput,
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
) -> workflow_run.WorkflowRun:
    logger = logging.getLogger()
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.WorkflowRun.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    workflow_version = await session.get_one(db.WorkflowVersion, input.workflow_version_id)
    manifest = Manifest.from_yaml(str(workflow_version.manifest))

    entity_inputs_list = [
        (ei.name, EntityInput(entity_type=ei.entity_type, entity_id=ei.entity_id)) for ei in input.entity_inputs or []
    ]
    entity_inputs = Manifest.normalize_inputs(entity_inputs_list)
    raw_inputs = json.loads(input.raw_input_json) if input.raw_input_json else {}

    input_errors = list(manifest.validate_inputs(entity_inputs, raw_inputs))
    if input_errors:
        # This is a client-input error
        logger.info(f"Invalid input: {', '.join(e.message() for e in input_errors)}")
        raise PlatformicsException(f"Invalid input: {', '.join(e.message() for e in input_errors)}")

    workflow_run = db.WorkflowRun(
        owner_user_id=int(principal.id),
        collection_id=input.collection_id,
        rails_workflow_run_id=input.rails_workflow_run_id,
        workflow_version_id=workflow_version.id,
        status=WorkflowRunStatus.CREATED,
        execution_id=None,
        raw_inputs_json=json.dumps(raw_inputs),
        entity_inputs=[
            db.WorkflowRunEntityInput(
                owner_user_id=int(principal.id),
                collection_id=input.collection_id,
                field_name=name,
                input_entity_id=ei.entity_id,
                entity_type=ei.entity_type,
            )
            for name, ei in entity_inputs_list
        ],
    )
    session.add(workflow_run)
    await session.commit()
    return workflow_run  # type: ignore


@strawberry.mutation(extensions=[DependencyExtension()])
async def create_workflow_run(
    input: RunWorkflowVersionInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
) -> workflow_run.WorkflowRun:
    return await _create_workflow_run(input, session=session, cerbos_client=cerbos_client, principal=principal)


async def _run_workflow_run(
    workflow_run_id: strawberry.ID,
    execution_id: typing.Optional[str],
    session: AsyncSession,
    cerbos_client: CerbosClient,
    principal: Principal,
    workflow_runner: WorkflowRunner,
    event_bus: EventBus,
    token: str,
) -> workflow_run.WorkflowRun:
    logger = logging.getLogger()
    workflow_run = await session.get_one(db.WorkflowRun, workflow_run_id)
    if not workflow_run:
        raise PlatformicsException(f"Workflow run {workflow_run_id} not found")
    attr = {"collection_id": workflow_run.collection_id}
    resource = Resource(id=str(workflow_run.id), kind=db.WorkflowRun.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("update", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot update entity in this collection")
    if workflow_run.status != WorkflowRunStatus.CREATED:
        raise PlatformicsException(f"Workflow run {workflow_run_id} is not in CREATED state")

    workflow_version = await session.get_one(db.WorkflowVersion, workflow_run.workflow_version_id)
    manifest = Manifest.from_yaml(str(workflow_version.manifest))
    workflow_entity_inputs = (
        await session.execute(
            select(db.WorkflowRunEntityInput).where(db.WorkflowRunEntityInput.workflow_run_id == workflow_run.id)
        )
    ).scalars()
    entity_inputs = Manifest.normalize_inputs(
        (e.field_name, EntityInput(entity_type=e.entity_type, entity_id=str(e.input_entity_id)))
        for e in workflow_entity_inputs
    )
    raw_inputs = json.loads(workflow_run.raw_inputs_json)
    workflow_runner_inputs_json = {}
    for input_loader_specifier in manifest.input_loaders:
        loader_entity_inputs = {
            k: entity_inputs[v] for k, v in input_loader_specifier.inputs.items() if v in entity_inputs
        }
        loader_raw_inputs = {k: raw_inputs[v] for k, v in input_loader_specifier.inputs.items() if v in raw_inputs}
        input_loader = resolve_input_loader(input_loader_specifier.name, input_loader_specifier.version)
        if not input_loader:
            logger.error(f"Input loader ({input_loader_specifier.name}, {input_loader_specifier.version}) not found")
            raise PlatformicsException("An error occurred while processing your inputs")

        input_loader_outputs = await input_loader(token).load(
            workflow_version, loader_entity_inputs, loader_raw_inputs, list(input_loader_specifier.outputs.keys())
        )
        for k, v in input_loader_specifier.outputs.items():
            if k not in input_loader_outputs:
                continue

            if v in workflow_runner_inputs_json:
                # This will only happen if loaders are misconfigured, it is an error on our side
                version_tuple = f"({input_loader_specifier.name}, {input_loader_specifier.version})"
                logger.error(f"Duplicate workflow input {v} for workflow {version_tuple}")
                raise PlatformicsException("An error occurred while processing your inputs")
            workflow_runner_inputs_json[v] = input_loader_outputs[k]

    status = WorkflowRunStatus.PENDING
    final_execution_id = execution_id
    try:
        if not final_execution_id:
            final_execution_id = await workflow_runner.run_workflow(
                event_bus=event_bus,
                workflow_path=workflow_version.workflow_uri,
                inputs=workflow_runner_inputs_json,
            )
    except Exception as e:
        logger.error(f"Failed to run workflow {workflow_version.id}: {e}")
        status = WorkflowRunStatus.FAILED
        await session.commit()
        raise PlatformicsException("Failed to run workflow")
    workflow_run.status = status
    workflow_run.workflow_runner_inputs_json = json.dumps(workflow_runner_inputs_json)
    workflow_run.started_at = datetime.now()
    if final_execution_id:
        workflow_run.execution_id = final_execution_id
    await session.commit()
    return workflow_run  # type: ignore


@strawberry.mutation(extensions=[DependencyExtension()])
async def run_workflow_run(
    workflow_run_id: strawberry.ID,
    execution_id: typing.Optional[str] = None,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    workflow_runner: WorkflowRunner = Depends(get_workflow_runner),
    event_bus: EventBus = Depends(get_event_bus),
    token: str = Depends(get_user_token),
) -> workflow_run.WorkflowRun:
    return await _run_workflow_run(
        workflow_run_id=workflow_run_id,
        execution_id=execution_id,
        session=session,
        cerbos_client=cerbos_client,
        principal=principal,
        workflow_runner=workflow_runner,
        event_bus=event_bus,
        token=token,
    )


@strawberry.mutation(extensions=[DependencyExtension()])
async def run_workflow_version(
    input: RunWorkflowVersionInput,
    execution_id: typing.Optional[str] = None,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    workflow_runner: WorkflowRunner = Depends(get_workflow_runner),
    event_bus: EventBus = Depends(get_event_bus),
    token: str = Depends(get_user_token),
) -> workflow_run.WorkflowRun:
    workflow_run = await _create_workflow_run(
        input,
        session=session,
        cerbos_client=cerbos_client,
        principal=principal,
    )
    return await _run_workflow_run(
        workflow_run_id=workflow_run.id,
        execution_id=execution_id,
        session=session,
        cerbos_client=cerbos_client,
        principal=principal,
        workflow_runner=workflow_runner,
        event_bus=event_bus,
        token=token,
    )


@strawberry.type
class Mutation(CodegenMutation):
    run_workflow_version: workflow_run.WorkflowRun = run_workflow_version
    create_workflow_run: workflow_run.WorkflowRun = create_workflow_run
    run_workflow_run: workflow_run.WorkflowRun = run_workflow_run


strawberry_config = StrawberryConfig(auto_camel_case=True, name_converter=CustomNameConverter())
schema = strawberry.Schema(query=Query, mutation=Mutation, config=strawberry_config)


def get_app() -> FastAPI:
    """
    Helper function that returns the app
    Ensures tests can get their own instances of the app
    """
    settings = APISettings.model_validate({})  # Workaround for https://github.com/pydantic/pydantic/issues/3753
    event_bus = load_event_bus(settings)
    workflow_runner = load_workflow_runner(settings)

    # strawberry graphql schema
    # start server with strawberry server app
    _app = FastAPI()
    # Add a global settings object to the app that we can use as a dependency
    _app.state.entities_settings = settings
    _app.state.event_bus = event_bus
    _app.state.workflow_runner = workflow_runner

    graphql_app: GraphQLRouter = GraphQLRouter(schema, context_getter=get_context, graphiql=True)
    _app.include_router(root_router)
    _app.include_router(graphql_app, prefix="/graphql")
    return _app


app = get_app()
