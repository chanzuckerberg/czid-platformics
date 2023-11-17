# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import factory
from database.models import SequencingRead
from test_infra.factories.main import CommonFactory, FileFactory
from test_infra.factories.sample import SampleFactory
from test_infra.factories.taxon import TaxonFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class SequencingReadFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = SequencingRead
        # Match entity_id with existing db rows to determine whether we should
        # create a new row or not.
        sqlalchemy_get_or_create = ("entity_id",)

    sample = factory.SubFactory(
        SampleFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    protocol = fuzzy.FuzzyChoice(["MNGS", "TARGETED", "MSSPE"])
    r1_file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="r1_file",
        file_format="fastq",
    )
    r2_file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="r2_file",
        file_format="fastq",
    )
    technology = fuzzy.FuzzyChoice(["Illumina", "Nanopore"])
    nucleic_acid = fuzzy.FuzzyChoice(["RNA", "DNA"])
    has_ercc = factory.Faker("boolean")
    taxon = factory.SubFactory(
        TaxonFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    primer_file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="primer_file",
        file_format="fastq",
    )