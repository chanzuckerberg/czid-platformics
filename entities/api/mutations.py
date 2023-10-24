import strawberry
import database.models as db
from api.files import File, create_file, upload_file, mark_upload_complete, MultipartUploadCredentials
from api.types.samples import Sample
from api.types.sequencing_reads import SequencingRead
from platformics.api.core.gql_loaders import get_base_creator, get_base_updater


@strawberry.type
class Mutation:
    # Create
    create_sample: Sample = get_base_creator(db.Sample, Sample)  # type: ignore
    create_sequencing_read: SequencingRead = get_base_creator(db.SequencingRead, SequencingRead)  # type: ignore
    # create_contig: Contig = get_base_creator(db.Contig, Contig)  # type: ignore

    # Update
    update_sample: Sample = get_base_updater(db.Sample, Sample)  # type: ignore

    # File management
    create_file: File = create_file
    upload_file: MultipartUploadCredentials = upload_file
    mark_upload_complete: File = mark_upload_complete
