import factory.random
from database.models import Sample, SequencingRead
from test_infra import factories as fa
from database.connect import SyncDB


# Tests
def test_samples(sync_db: SyncDB) -> None:
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        factory.random.reseed_random(123)
        fa.SampleFactory.create_batch(2, location="San Francisco, CA")
        fa.SampleFactory.create_batch(5, location="Mountain View, CA")

        assert session.query(Sample).filter_by(location="Mountain View, CA").count() == 5


# Test linking SequencingReads to Samples
def test_reads(sync_db: SyncDB) -> None:
    with sync_db.session() as session:
        fa.SessionStorage.set_session(session)
        factory.random.reseed_random(123)

        sample1 = fa.SampleFactory(name="Sample 1")
        sample2 = fa.SampleFactory(name="Sample 2")
        fa.SequencingReadFactory.create_batch(2, sample=sample1, protocol="MNGS", nucleotide="DNA")
        fa.SequencingReadFactory.create_batch(3, sample=sample2, protocol="TARGETED", nucleotide="DNA")

        assert session.query(SequencingRead).filter_by(sample_id=sample1.entity_id).count() == 2
        assert session.query(SequencingRead).filter_by(sample_id=sample2.entity_id).count() == 3
