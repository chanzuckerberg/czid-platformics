import factory.random
from factoryboy import workflow_factory as wf
from platformics.api.core.settings import APISettings
from platformics.database.connect import init_sync_db


def use_factoryboy():
    settings = APISettings.parse_obj({})
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    wf.SessionStorage.set_session(session)
    factory.random.reseed_random(1234567)

    wf.WorkflowFactory.create_batch(4)

    wf.WorkflowVersionFactory.create()

    wf.RunFactory.create_batch(5)
    session.commit()


if __name__ == "__main__":
    use_factoryboy()
