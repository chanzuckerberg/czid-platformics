"""
Factory for generating ConsensusGenome objects.

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long

import factory
from database.models import ConsensusGenome
from test_infra.factories.main import CommonFactory, FileFactory
from test_infra.factories.taxon import TaxonFactory
from test_infra.factories.sequencing_read import SequencingReadFactory
from test_infra.factories.reference_genome import ReferenceGenomeFactory
from test_infra.factories.accession import AccessionFactory
from factory import Faker
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class ConsensusGenomeFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = ConsensusGenome
        # Match entity_id with existing db rows to determine whether we should
        # create a new row or not.
        sqlalchemy_get_or_create = ("entity_id",)

    taxon = factory.SubFactory(
        TaxonFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    sequencing_read = factory.SubFactory(
        SequencingReadFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    reference_genome = factory.SubFactory(
        ReferenceGenomeFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    accession = factory.SubFactory(
        AccessionFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    sequence = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="sequence",
        file_format="fastq",
    )
    intermediate_outputs = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="intermediate_outputs",
        file_format="fastq",
    )
