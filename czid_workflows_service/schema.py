from typing import Any, Callable, Sequence, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import models
import strawberry
from strawberry.types import Info
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView


from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyLoader, StrawberrySQLAlchemyMapper

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
models.Base.metadata.create_all(engine)
session = Session(engine)

strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()
@strawberry_sqlalchemy_mapper.type(models.Workflow)
class Workflow:
    pass


@strawberry_sqlalchemy_mapper.type(models.WorkflowVersion)
class WorkflowVersion:
    pass


@strawberry_sqlalchemy_mapper.type(models.Run)
class Run:
    pass


def with_loader(func):
    def wrapper(self, info: Info):
        info.context["sqlalchemy_loader"] = StrawberrySQLAlchemyLoader(bind=session)
        return func(self, info)
    return wrapper

T = TypeVar("T")
R = TypeVar("R")
def with_loader(func: Callable[R, T]) -> Callable[R, T]:
    def wrapper(self, info: Info, **kwargs) -> Sequence[T]:
        info.context["sqlalchemy_loader"] = StrawberrySQLAlchemyLoader(bind=session)
        return func(self, info)
    return wrapper


@strawberry.type
class Query:
    @strawberry.field
    @with_loader
    def workflows(self, **kwargs) -> Sequence[Workflow]:
        return session.scalars(session.query(models.Workflow)).all()

    @strawberry.field
    def workflow_versions(self) -> Sequence[WorkflowVersion]:
        return session.scalars(session.query(models.WorkflowVersion)).all()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_workflow(self, name: str, defaultVersion: str, minimumSupportedVersion: str) -> Workflow:
        workflow = models.Workflow(name=name, default_version=defaultVersion, minimum_supported_version=minimumSupportedVersion)
        session.add(workflow)
        session.commit()
        return workflow
    
    @strawberry.mutation
    def add_workflow_version(self, workflowId: str, version: str, workflowType: str, packageUri: str, beta: bool, deprecated: bool, graphJson: str) -> WorkflowVersion:
        workflowVersion = models.WorkflowVersion(workflow_id=workflowId, version=version, workflow_type=workflowType, package_uri=packageUri, beta=beta, deprecated=deprecated, graph_json=graphJson)
        session.add(workflowVersion)
        session.commit()
        return workflowVersion

    @strawberry.mutation
    def add_run(self, userId: str, executionId: str, inputsJson: str, workflowVersionId: str) -> Run:
        run = models.Run(user_id=userId, execution_id=executionId, inputs_json=inputsJson, workflow_version_id=workflowVersionId)
        session.add(run)
        session.commit()
        return run

app = web.Application()


strawberry_sqlalchemy_mapper.finalize()
# only needed if you have polymorphic types
additional_types = list(strawberry_sqlalchemy_mapper.mapped_types.values())
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    types=additional_types,
)


app.router.add_route("*", "/graphql", GraphQLView(schema=schema))