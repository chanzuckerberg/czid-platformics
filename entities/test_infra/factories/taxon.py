"""
Factory for generating Taxon objects.

Auto-generated by running 'make codegen'. Do not edit.
Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.
"""

# ruff: noqa: E501 Line too long

import factory
from database.models import Taxon
from test_infra.factories.main import CommonFactory
from test_infra.factories.upstream_database import UpstreamDatabaseFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class TaxonFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = Taxon
        # Match entity_id with existing db rows to determine whether we should
        # create a new row or not.
        sqlalchemy_get_or_create = ("entity_id",)

    wikipedia_id = fuzzy.FuzzyText()
    description = fuzzy.FuzzyText()
    common_name = fuzzy.FuzzyText()
    name = fuzzy.FuzzyText()
    is_phage = factory.Faker("boolean")
    upstream_database = factory.SubFactory(
        UpstreamDatabaseFactory,
        owner_user_id=factory.SelfAttribute("..owner_user_id"),
        collection_id=factory.SelfAttribute("..collection_id"),
    )
    upstream_database_identifier = fuzzy.FuzzyText()
    level = fuzzy.FuzzyChoice(
        [
            "level_sublevel",
            "level_species",
            "level_genus",
            "level_family",
            "level_order",
            "level_class",
            "level_phylum",
            "level_kingdom",
            "level_superkingdom",
        ]
    )
    tax_parent = None
    tax_species = None
    tax_genus = None
    tax_family = None
    tax_order = None
    tax_class = None
    tax_phylum = None
    tax_kingdom = None
    tax_superkingdom = None
