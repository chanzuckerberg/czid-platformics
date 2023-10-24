import datetime
import factory
import sqlalchemy as sa
from factory import fuzzy


from database.models import Workflow, WorkflowVersion, Run, RunStatus


""" ABSTRACT THIS OUT """


class SessionStorage:
    session = None

    @classmethod
    def set_session(cls, session: sa.orm.Session) -> None:
        cls.session = session

    @classmethod
    def get_session(cls) -> sa.orm.Session | None:
        return cls.session


class CommonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session_factory = SessionStorage.get_session
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = None  # workaround for a bug in factoryboy


class WorkflowFactory(CommonFactory):
    class Meta:
        model = Workflow
        sqlalchemy_session = None

    name = factory.Sequence(lambda n: "mngs-pipeline-%s" % n)
    default_version = factory.Sequence(lambda n: "v1.0.%s" % n)
    minimum_supported_version = factory.LazyAttribute(lambda o: "%s" % o.default_version)


class WorkflowVersionFactory(CommonFactory):
    class Meta:
        model = WorkflowVersion
        sqlalchemy_session = None

    # version = factory.Sequence(lambda n: "v1.0.%s" % n)
    # type = factory.fuzzy.FuzzyChoice(["WDL", "SMK", "NF"])
    # package_uri = factory.LazyAttribute(lambda n: f"s3://path/to/workflow-{n.version}/run.{n.type.lower()}")
    # beta = Faker("pybool")
    # deprecated = Faker("pybool")
    # graph_json = fuzzy.FuzzyChoice(["{}"])
    workflow = factory.SubFactory(WorkflowFactory)
    manifest = factory.LazyAttribute(lambda n: open("/workflows/manifests/first_workflow_manifest.json").read())


class RunFactory(CommonFactory):
    class Meta:
        model = Run
        sqlalchemy_session = None

    user_id = factory.Sequence(int)
    project_id = factory.Sequence(int)
    started_at = fuzzy.FuzzyDateTime(datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC))
    ended_at = factory.LazyAttribute(lambda n: n.started_at + datetime.timedelta(hours=5))
    execution_id = fuzzy.FuzzyText()
    inputs_json = fuzzy.FuzzyChoice(["{}"])
    outputs_json = fuzzy.FuzzyChoice(["{}"])
    status = fuzzy.FuzzyChoice(RunStatus)
    workflow_version = factory.SubFactory(WorkflowVersionFactory)
