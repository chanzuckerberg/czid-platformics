import factory.random
from settings import APISettings
from platformics.database.connect import init_sync_db
from api.manifest import import_manifests
from test_infra.factories.main import SessionStorage
from test_infra.factories.workflow import WorkflowFactory
from test_infra.factories.workflow_version import WorkflowVersionFactory
from test_infra.factories.run import RunFactory


def use_factoryboy() -> None:
    settings = APISettings.model_validate({})
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    SessionStorage.set_session(session)

    # import manifests
    import_manifests(session=session)

    factory.random.reseed_random(1234567)

    WorkflowFactory.create_batch(4)

    WorkflowVersionFactory.create()

    RunFactory.create_batch(5)
    session.commit()


if __name__ == "__main__":
    use_factoryboy()
