import strawberry
from typing import Sequence
from api.files import File, create_file, upload_file, mark_upload_complete, MultipartUploadResponse
from api.types.sample import Sample, create_sample, update_sample, delete_sample

@strawberry.type
class Mutation:
    # File mutations
    create_file: File = create_file
    upload_file: MultipartUploadResponse = upload_file
    mark_upload_complete: File = mark_upload_complete

    # Entity mutations
    create_sample: Sample = create_sample
    update_sample: Sequence[Sample] = update_sample
    delete_sample: Sequence[Sample] = delete_sample
