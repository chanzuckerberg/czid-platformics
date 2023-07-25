from database.connect import init_sync_db
from test_infra import factories as fa
import factory.random

def use_factoryboy():
    app_db = init_sync_db()
    session = app_db.session()
    fa.SessionStorage.set_session(session)
    factory.random.reseed_random(1234567)

    # Create some samples with one SequencingRead each
    fa.SequencingReadFactory.create_batch(5)

    # create some samples with multiple SequencingReads
    sa1 = fa.SampleFactory()
    sa2 = fa.SampleFactory()

    fa.SequencingReadFactory.create_batch(3, sample=sa1)
    fa.SequencingReadFactory.create_batch(2, sample=sa2)

    session.commit()


if __name__ == "__main__":
    use_factoryboy()
