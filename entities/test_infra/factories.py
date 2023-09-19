import factory
import sqlalchemy as sa
from database.models import File, FileStatus, Sample, SequencingRead
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


# TODO, this is a lame singleton to prevent this library from
# requiring an active SA session at import-time. We should try
# to refactor it out when we know more about factoryboy
class SessionStorage:
    session = None

    @classmethod
    def set_session(cls, session: sa.orm.Session) -> None:
        cls.session = session

    @classmethod
    def get_session(cls) -> sa.orm.Session | None:
        return cls.session


class CommonFactory(factory.alchemy.SQLAlchemyModelFactory):
    owner_user_id = fuzzy.FuzzyInteger(1, 1000)
    collection_id = fuzzy.FuzzyInteger(1, 1000)

    class Meta:
        sqlalchemy_session_factory = SessionStorage.get_session
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = None  # workaround for a bug in factoryboy


class FileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session_factory = SessionStorage.get_session
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = File
        # What fields do we try to match to existing db rows to determine whether we
        # should create a new row or not?
        sqlalchemy_get_or_create = ("namespace", "path")
        # exclude = ("sample_organ",)

    status = factory.Faker("enum", enum_cls=FileStatus)
    protocol = fuzzy.FuzzyChoice(["S3", "GCP"])
    namespace = fuzzy.FuzzyChoice(["bucket_1", "bucket_2"])
    # path = factory.LazyAttribute(lambda o: {factory.Faker("file_path", depth=3, extension=o.file_format)})
    path = factory.Faker("file_path", depth=3)
    file_format = fuzzy.FuzzyChoice(["fasta", "fastq", "bam"])
    compression_type = fuzzy.FuzzyChoice(["gz", "bz2", "xz"])
    size = fuzzy.FuzzyInteger(1024, 1024 * 1024 * 1024)  # Between 1k and 1G

    @classmethod
    def update_file_ids(cls) -> None:
        session = SessionStorage.get_session()
        if not session:
            raise Exception("No session found")
        session.execute(
            sa.text(
                "UPDATE sequencing_read SET sequence_file_id = file.id "
                "FROM file WHERE sequencing_read.entity_id = file.entity_id",
            )
        )
        session.commit()


class SampleFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = Sample
        # What fields do we try to match to existing db rows to determine whether we
        # should create a new row or not?
        sqlalchemy_get_or_create = ("name", "location")

        # The field in the exclusion list are for internal use only and don't get
        # persisted to the db.
        exclude = ("sample_organ",)

    # This is in the exclusion list so it doesn't get added to our db model.
    sample_organ = factory.Faker("organ")

    name = factory.LazyAttribute(lambda o: "Sample %s" % o.sample_organ)
    location = factory.Faker("city")


class SequencingReadFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = SequencingRead
        sqlalchemy_get_or_create = (
            "nucleotide",
            "sequence",
            "protocol",
        )

    sample = factory.SubFactory(
        SampleFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    nucleotide = fuzzy.FuzzyChoice(["RNA", "DNA"])
    # Workaround for a bug in bioseq's handling of randomness and DNA string generation.
    sequence = fuzzy.FuzzyText(length=100, chars="ACTG")
    # sequence = factory.Faker('dna', length=100)
    protocol = fuzzy.FuzzyChoice(["TARGETED", "MNGS", "MSSPE"])

    sequencing_read_file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="sequence_file",
        file_format="fastq",
    )
