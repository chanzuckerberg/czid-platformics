import typing
import strawberry
from strawberry import relay
from api.types.sample import Sample, resolve_sample
from api.types.sequencing_read import SequencingRead, resolve_sequencing_read
from api.types.contig import Contig, resolve_contig
from api.files import File, resolve_files


@strawberry.type
class Query:
    # Allow queries by node ID
    node: relay.Node = relay.node()

    samples: typing.Sequence[Sample] = resolve_sample
    sequencing_reads: typing.Sequence[SequencingRead] = resolve_sequencing_read
    contigs: typing.Sequence[Contig] = resolve_contig
    files: typing.Sequence[File] = resolve_files
