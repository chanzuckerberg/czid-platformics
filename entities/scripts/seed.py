from database.connect import init_sync_db
from test_infra import factories as fa
import factory.random
from api.core.settings import CLISettings


def use_factoryboy():
    settings = CLISettings()
    app_db = init_sync_db(settings.SYNC_DB_URI)
    session = app_db.session()
    fa.SessionStorage.set_session(session)
    factory.random.reseed_random(1234567)

    # Create some samples with one SequencingRead each
    fa.SequencingReadFactory.create_batch(5, owner_user_id=111, collection_id=444)
    fa.SequencingReadFactory.create_batch(5, owner_user_id=222, collection_id=555)

    # create some samples with multiple SequencingReads
    sa1 = fa.SampleFactory(owner_user_id=222, collection_id=555)
    sa2 = fa.SampleFactory(owner_user_id=333, collection_id=666)

    fa.SequencingReadFactory.create_batch(
        3, sample=sa1, owner_user_id=sa1.owner_user_id, collection_id=sa1.collection_id
    )
    fa.SequencingReadFactory.create_batch(
        2, sample=sa2, owner_user_id=sa2.owner_user_id, collection_id=sa2.collection_id
    )

    session.commit()


if __name__ == "__main__":
    use_factoryboy()
