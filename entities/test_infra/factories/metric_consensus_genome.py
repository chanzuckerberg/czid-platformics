# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import factory
from database.models import MetricConsensusGenome
from test_infra.factories.main import CommonFactory, FileFactory
from test_infra.factories.consensus_genome import ConsensusGenomeFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class MetricConsensusGenomeFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = MetricConsensusGenome
        # TODO:
        # What fields do we try to match to existing db rows to determine whether we
        # should create a new row or not?
        # sqlalchemy_get_or_create = ("name", "collection_location")
    consensus_genome = factory.SubFactory(
        ConsensusGenomeFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    coverage_depth = factory.Faker("float") 
    reference_genome_length = factory.Faker("float") 
    percent_genome_called = factory.Faker("float") 
    percent_identity = factory.Faker("float") 
    gc_percent = factory.Faker("float") 
    total_reads = factory.Faker("int") 
    mapped_reads = factory.Faker("int") 
    ref_snps = factory.Faker("int") 
    n_actg = factory.Faker("int") 
    n_missing = factory.Faker("int") 
    n_ambiguous = factory.Faker("int") 
    coverage_viz_summary_file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="coverage_viz_summary_file",
        file_format="fastq", 
    )