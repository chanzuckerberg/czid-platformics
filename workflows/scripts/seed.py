from database.connect import init_sync_db
from factoryboy import workflow_factory as wf
import factory.random

def use_factoryboy():
    app_db = init_sync_db()
    session = app_db.session()
    wf.SessionStorage.set_session(session)
    factory.random.reseed_random(1234567)

    wf.WorkflowFactory.create_batch(4)
    # Create some samples with one SequencingRead each

    wf.WorkflowVersionFactory.create()

    wf.RunFactory.create_batch(5)
    # create some samples with multiple SequencingReads
    session.commit()


if __name__ == "__main__":
    use_factoryboy()
