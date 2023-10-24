import factory.random
from factoryboy import workflow_factory as wf
from settings import APISettings
from platformics.database.connect import init_sync_db
from manifest import import_manifests


def use_factoryboy() -> None:
    settings = APISettings.model_validate({})
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    wf.SessionStorage.set_session(session)

    # import manifests
    import_manifests(session=session)

    factory.random.reseed_random(1234567)

    wf.WorkflowFactory.create_batch(4)

    wf.WorkflowVersionFactory.create()

    wf.RunFactory.create_batch(5)
    session.commit()


if __name__ == "__main__":
    use_factoryboy()
