"""
Factory for generating PhylogeneticTree objects.

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long

import factory
from database.models import PhylogeneticTree
from test_infra.factories.main import CommonFactory, FileFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class PhylogeneticTreeFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = PhylogeneticTree
        # Match entity_id with existing db rows to determine whether we should
        # create a new row or not.
        sqlalchemy_get_or_create = ("entity_id",)

    tree = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="tree",
        file_format="fastq",
    )
    format = fuzzy.FuzzyChoice(["newick", "auspice_v1", "auspice_v2"])