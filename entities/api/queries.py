import typing

import database.models as db
from platformics.api.core.gql_loaders import get_base_loader, get_file_loader

import strawberry
from api.files import File
from api.types.samples import Sample, resolve_samples
from api.types.sequencing_reads import SequencingRead, resolve_sequencing_reads


@strawberry.type
class Query:
    samples: typing.Sequence[Sample] = resolve_samples
    sequencing_reads: typing.Sequence[SequencingRead] = resolve_sequencing_reads
    files: typing.Sequence[File] = get_file_loader(db.File, File)
