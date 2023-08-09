import factory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ

from database.models import Sample, SequencingRead

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)

# TODO, this is a lame singleton to prevent this library from
# requiring an active SA session at import-time. We should try
# to refactor it out when we know more about factoryboy
class SessionStorage:
    session = None

    @classmethod
    def set_session(cls, session):
        cls.session = session

    @classmethod
    def get_session(cls):
        return cls.session


class CommonFactory(factory.alchemy.SQLAlchemyModelFactory):
    owner_user_id = fuzzy.FuzzyInteger(1, 1000)
    collection_id = fuzzy.FuzzyInteger(1, 1000)
    class Meta:
        sqlalchemy_session_factory = SessionStorage.get_session
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = None  # workaround for a bug in factoryboy

class SampleFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = Sample
        # What fields do we try to match to existing db rows to determine whether we
        # should create a new row or not?
        sqlalchemy_get_or_create = ('name', 'location')

        # The field in the exclusion list are for internal use only and don't get
        # persisted to the db.
        exclude = ('sample_organ',)

    # This is in the exclusion list so it doesn't get added to our db model.
    sample_organ = factory.Faker('organ')

    name = factory.LazyAttribute(lambda o: 'Sample %s' % o.sample_organ)
    location = factory.Faker('city')


class SequencingReadFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = SequencingRead
        sqlalchemy_get_or_create = ('nucleotide', 'sequence', 'protocol',)

    sample = factory.SubFactory(SampleFactory, owner_user_id=factory.SelfAttribute("..owner_user_id"), collection_id=factory.SelfAttribute("..collection_id"))
    nucleotide = fuzzy.FuzzyChoice(['RNA', 'DNA'])
    # Workaround for a bug in bioseq's handling of randomness and DNA string generation.
    sequence = fuzzy.FuzzyText(length=100, chars="ACTG")
    # sequence = factory.Faker('dna', length=100)
    protocol = fuzzy.FuzzyChoice(['TARGETED', 'MNGS', 'MSSPE'])
