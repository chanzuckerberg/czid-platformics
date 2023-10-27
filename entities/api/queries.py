import typing
import strawberry

# from api.files import File
from api.types.samples import Sample, resolve_samples
from api.types.sequencing_reads import SequencingRead, resolve_sequencing_reads
from api.types.contigs import Contig, resolve_contigs


@strawberry.type
class Query:
    samples: typing.Sequence[Sample] = resolve_samples
    sequencing_reads: typing.Sequence[SequencingRead] = resolve_sequencing_reads
    contigs: typing.Sequence[Contig] = resolve_contigs
    # files: typing.Sequence[File] = get_file_loader(db.File, File)
