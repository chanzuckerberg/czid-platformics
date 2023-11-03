import typing
import strawberry

from api.types.samples import Sample, resolve_samples
from api.types.sequencing_reads import SequencingRead, resolve_sequencing_reads
from api.types.contigs import Contig, resolve_contigs
from api.files import File, resolve_files


@strawberry.type
class Query:
    samples: typing.Sequence[Sample] = resolve_samples
    sequencing_reads: typing.Sequence[SequencingRead] = resolve_sequencing_reads
    contigs: typing.Sequence[Contig] = resolve_contigs
    files: typing.Sequence[File] = resolve_files
