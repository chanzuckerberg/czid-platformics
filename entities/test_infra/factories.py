import factory
import faker
import sqlalchemy as sa
from database.models import File, FileStatus, Sample, SequencingRead
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


def generate_relative_file_path(obj) -> str:  # type: ignore
    fake = faker.Faker()
    # Can't use absolute=True param because that requires newer version of faker than faker-biology supports
    return fake.file_path(depth=3, extension=obj.file_format).lstrip("/")


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

    status = factory.Faker("enum", enum_cls=FileStatus)
    protocol = fuzzy.FuzzyChoice(["S3", "GCP"])
    namespace = fuzzy.FuzzyChoice(["local-bucket", "remote-bucket"])
    path = factory.LazyAttribute(lambda o: generate_relative_file_path(o))
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
                "UPDATE sequencing_read SET r1_file_id = file.id "
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
        sqlalchemy_get_or_create = ("name", "collection_location")

    sample_type = factory.Faker("organ")
    name = factory.LazyAttribute(lambda o: "Sample %s" % o.sample_type)
    collection_location = factory.Faker("city")
    water_control = factory.Faker("boolean")


class SequencingReadFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = SequencingRead

    sample = factory.SubFactory(
        SampleFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    nucleic_acid = fuzzy.FuzzyChoice(["RNA", "DNA"])
    protocol = fuzzy.FuzzyChoice(["TARGETED", "MNGS", "MSSPE"])
    technology = fuzzy.FuzzyChoice(["Illumina", "Nanopore"])
    has_ercc = factory.Faker("boolean")
    r1_file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="r1_file",
        file_format="fastq",
    )
