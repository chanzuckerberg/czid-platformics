import typing
import strawberry
<<<<<<< HEAD
from strawberry import relay
from api.types.samples import Sample, resolve_samples
from api.types.sequencing_reads import SequencingRead, resolve_sequencing_reads
from api.types.contigs import Contig, resolve_contigs
=======

from api.types.sample import Sample, resolve_sample
from api.types.sequencing_read import SequencingRead, resolve_sequencing_read
from api.types.contig import Contig, resolve_contig
>>>>>>> ca0304c (update templates)
from api.files import File, resolve_files


@strawberry.type
class Query:
<<<<<<< HEAD
    # Allow queries by node ID
    node: relay.Node = relay.node()

    # Queries for each entity
    samples: typing.Sequence[Sample] = resolve_samples
    sequencing_reads: typing.Sequence[SequencingRead] = resolve_sequencing_reads
    contigs: typing.Sequence[Contig] = resolve_contigs
=======
    samples: typing.Sequence[Sample] = resolve_sample
    sequencing_reads: typing.Sequence[SequencingRead] = resolve_sequencing_read
    contigs: typing.Sequence[Contig] = resolve_contig
>>>>>>> ca0304c (update templates)
    files: typing.Sequence[File] = resolve_files
