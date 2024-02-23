"""
Factory for generating HostOrganism objects.

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long

import factory
from database.models import HostOrganism
from test_infra.factories.main import CommonFactory, FileFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class HostOrganismFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = HostOrganism
        # Match entity_id with existing db rows to determine whether we should
        # create a new row or not.
        sqlalchemy_get_or_create = ("entity_id",)

    rails_host_genome_id = fuzzy.FuzzyInteger(1, 1000)
    name = fuzzy.FuzzyText()
    version = fuzzy.FuzzyText()
    category = fuzzy.FuzzyChoice(["human", "insect", "non_human_animal", "unknown"])
    is_deuterostome = factory.Faker("boolean")
    sequence = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="sequence",
        file_format="fastq",
    )
