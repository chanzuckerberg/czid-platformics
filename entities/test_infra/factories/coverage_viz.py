# Auto-generated by running 'make codegen'. Do not edit.
# Make changes to the template codegen/templates/test_infra/factories/class_name.py.j2 instead.

# ruff: noqa: E501 Line too long

import factory
from database.models import CoverageViz
from test_infra.factories.main import CommonFactory, FileFactory
from factory import Faker, fuzzy
from faker_biology.bioseq import Bioseq
from faker_biology.physiology import Organ
from faker_enum import EnumProvider

Faker.add_provider(Bioseq)
Faker.add_provider(Organ)
Faker.add_provider(EnumProvider)


class CoverageVizFactory(CommonFactory):
    class Meta:
        sqlalchemy_session = None  # workaround for a bug in factoryboy
        model = CoverageViz
        # TODO:
        # What fields do we try to match to existing db rows to determine whether we
        # should create a new row or not?
        # sqlalchemy_get_or_create = ("name", "collection_location")
    accession_id = factory.Faker("string") 
    coverage_viz_file = factory.RelatedFactory(
        FileFactory,
        factory_related_name="entity",
        entity_field_name="coverage_viz_file",
        file_format="fastq", 
    )