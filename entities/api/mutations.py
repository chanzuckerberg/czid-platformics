import strawberry

@strawberry.type
class Mutation:
    # Create
    create_sample: Sample = get_base_creator(db.Sample, Sample)  # type: ignore
    create_sequencing_read: SequencingRead = get_base_creator(db.SequencingRead, SequencingRead)  # type: ignore
    create_contig: Contig = get_base_creator(db.Contig, Contig)  # type: ignore

    # Update
    update_sample: Sample = get_base_updater(db.Sample, Sample)  # type: ignore

    # File management
    create_file: SignedURL = create_file
    mark_upload_complete: File = mark_upload_complete

