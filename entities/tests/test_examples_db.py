import factory.random
from database.models import Sample
from test_infra import factories as fa

# Tests
def test_samples(postgresql):
    with postgresql() as session:
        fa.SessionStorage.set_session(session)
        factory.random.reseed_random(123)
        fa.SampleFactory.create_batch(2, location="San Francisco, CA")
        fa.SampleFactory.create_batch(5, location="Mountain View, CA")

        assert session.query(Sample).filter_by(location="Mountain View, CA").count() == 5
