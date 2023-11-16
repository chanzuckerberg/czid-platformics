import factory.random
from database.models import Sample, SequencingRead
from test_infra.factories.main import SessionStorage
from test_infra.factories.sample import SampleFactory
from test_infra.factories.sequencing_read import SequencingReadFactory
from platformics.database.connect import SyncDB


# Tests
def test_samples(sync_db: SyncDB) -> None:
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        factory.random.reseed_random(123)
        SampleFactory.create_batch(2, collection_location="San Francisco, CA")
        SampleFactory.create_batch(5, collection_location="Mountain View, CA")

        assert session.query(Sample).filter_by(collection_location="Mountain View, CA").count() == 5


# Test linking SequencingReads to Samples
def test_reads(sync_db: SyncDB) -> None:
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        factory.random.reseed_random(123)

        sample1 = SampleFactory(name="Sample 1")
        sample2 = SampleFactory(name="Sample 2")
        SequencingReadFactory.create_batch(2, sample=sample1, protocol="MNGS", nucleic_acid="DNA")
        SequencingReadFactory.create_batch(3, sample=sample2, protocol="TARGETED", nucleic_acid="DNA")

        assert session.query(SequencingRead).filter_by(sample_id=sample1.entity_id).count() == 2
        assert session.query(SequencingRead).filter_by(sample_id=sample2.entity_id).count() == 3
