# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import factory
from database.models import MetadataField
from test_infra.factories.main import CommonFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class MetadataFieldFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = MetadataField
        # Match entity_id with existing db rows to determine whether we should
        # create a new row or not.
        sqlalchemy_get_or_create = ("entity_id",)

    field_name = fuzzy.FuzzyText()
    description = fuzzy.FuzzyText()
    field_type = fuzzy.FuzzyText()
    is_required = factory.Faker("boolean")
    options = fuzzy.FuzzyText()
    default_value = fuzzy.FuzzyText()
