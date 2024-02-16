"""
GraphQL web app runner
"""
import json
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
    require_auth_principal,
)
from platformics.api.core.errors import PlatformicsException
from platformics.api.core.strawberry_extensions import DependencyExtension
from platformics.database.connect import AsyncDB
from plugins.plugin_types import EventBus, WorkflowRunner
from settings import APISettings
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from strawberry.schema.name_converter import HasGraphQLName, NameConverter

from api.config import load_event_bus, load_workflow_runner, resolve_input_loader
from api.core.gql_loaders import WorkflowLoader
from api.mutations import Mutation as CodegenMutation
from api.queries import Query
from api.types import workflow_run

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
        "sqlalchemy_loader": WorkflowLoader(engine=engine, cerbos_client=cerbos_client, principal=principal),
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


@strawberry.mutation(extensions=[DependencyExtension()])
async def run_workflow_version(
    input: RunWorkflowVersionInput,
    session: AsyncSession = Depends(get_db_session, use_cache=False),
    cerbos_client: CerbosClient = Depends(get_cerbos_client),
    principal: Principal = Depends(require_auth_principal),
    workflow_runner: WorkflowRunner = Depends(get_workflow_runner),
    event_bus: EventBus = Depends(get_event_bus),
) -> workflow_run.WorkflowRun:
    attr = {"collection_id": input.collection_id}
    resource = Resource(id="NEW_ID", kind=db.WorkflowRunStep.__tablename__, attr=attr)
    if not cerbos_client.is_allowed("create", principal, resource):
        raise PlatformicsException("Unauthorized: Cannot create entity in this collection")

    workflow_version = await session.get_one(db.WorkflowVersion, input.workflow_version_id)
    manifest = Manifest.from_yaml(str(workflow_version.manifest))

    entity_inputs = {
        entity_input.name: EntityInput(entity_type=entity_input.entity_type, entity_id=entity_input.entity_id)
        for entity_input in input.entity_inputs or []
    }
    raw_inputs = json.loads(input.raw_input_json) if input.raw_input_json else {}

    input_errors = list(manifest.validate_inputs(entity_inputs, raw_inputs))
    if input_errors:
        raise PlatformicsException(f"Invalid input: {', '.join([str(input_error) for input_error in input_errors])}")

    raw_inputs_json = {}
    for input_loader_specifier in manifest.input_loaders:
        loader_entity_inputs = {
            k: entity_inputs[v] for k, v in input_loader_specifier.inputs.items() if v in entity_inputs
        }
        loader_raw_inputs = {k: raw_inputs[v] for k, v in input_loader_specifier.inputs.items() if v in raw_inputs}
        input_loader = resolve_input_loader(input_loader_specifier.name, input_loader_specifier.version)
        if not input_loader:
            raise PlatformicsException(f"Input loader {input_loader_specifier.name} not found")

        input_loader_outputs = await input_loader.load(
            workflow_version, loader_entity_inputs, loader_raw_inputs, list(input_loader_specifier.outputs.keys())
        )
        for k, v in input_loader_specifier.outputs.items():
            if k not in input_loader_outputs:
                loader_label = f"{input_loader_specifier.name} ({input_loader_specifier.version})"
                raise PlatformicsException(f"Input loader  {loader_label}) did not produce output {k}")

            if v in entity_inputs:
                raise PlatformicsException(f"Duplicate raw input {v}")
            raw_inputs_json[v] = input_loader_outputs[k]

    status = "PENDING"
    execution_id = None
    try:
        execution_id = await workflow_runner.run_workflow(
            event_bus=event_bus,
            workflow_path=workflow_version.workflow_uri,
            inputs=raw_inputs_json,
        )
    except Exception:
        status = "FAILED"

    workflow_run = db.WorkflowRun(
        owner_user_id=int(principal.id),
        collection_id=input.collection_id,
        workflow_version_id=workflow_version.id,
        status=status,
        execution_id=execution_id,
        raw_inputs_json=json.dumps(raw_inputs_json),
        entity_inputs=[
            db.WorkflowRunEntityInput(
                owner_user_id=int(principal.id),
                collection_id=input.collection_id,
                field_name=k,
                input_entity_id=v.entity_id,
                entity_type=v.entity_type,
            )
            for k, v in entity_inputs.items()
        ],
    )
    session.add(workflow_run)
    await session.commit()
    return workflow_run  # type: ignore


@strawberry.type
class Mutation(CodegenMutation):
    RunWorkflow: workflow_run.WorkflowRun = run_workflow_version


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
