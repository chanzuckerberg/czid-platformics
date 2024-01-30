"""
Factory for generating ReferenceGenome objects.

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long

import factory
from database.models import ReferenceGenome
from test_infra.factories.main import CommonFactory, FileFactory
from test_infra.factories.taxon import TaxonFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class ReferenceGenomeFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = ReferenceGenome
        # Match entity_id with existing db rows to determine whether we should
        # create a new row or not.
        sqlalchemy_get_or_create = ("entity_id",)

    file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="file",
        file_format="fastq",
    )
    taxon = factory.SubFactory(
        TaxonFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    accession_id = fuzzy.FuzzyText()
    accession_name = fuzzy.FuzzyText()
