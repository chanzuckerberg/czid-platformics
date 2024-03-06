import json

from database.models import Entity
from database.models.file import File

from platformics.util.seed_utils import (
    TEST_USER_ID,
    SeedSession,
)
from support.enums import FileAccessProtocol


def main() -> tuple[list[dict[str, str]], dict[str, str]]:
    """
    An idempotent seed script to create the minimum viable set of entities to run consensus genomes

    It also creates entity and raw inputs to run the consensus genome workflow
    """
    session = SeedSession()

    files = (
        session.query(File)
        .join(Entity, File.entity_id == Entity.id)
        .filter(
            Entity.owner_user_id == TEST_USER_ID,
        )
        .all()
    )

    # redo above joining File on Entity by
    file_ids: list[dict[str, str]] = []
    for file in files:
        if file.protocol == FileAccessProtocol.s3 and session.s3_local:
            session.upsert_bucket(file.namespace)
            print(f"Creating file {file.id} in {file.namespace}/{file.path}")
            session.s3_local.put_object(Bucket=file.namespace, Key=file.path, Body="ABC")
        if len(file_ids) < 4:
            file_ids.append({"name": "files", "entity_type": "file", "entity_id": str(file.id)})

    return file_ids, {
        "bulk_download_type": "zip",
        "download_display_name": "Test",
    }


if __name__ == "__main__":
    print("Seeding database for bulk downloads workflow")
    entity_inputs, raw_inputs = main()
    print("entityInputs", json.dumps(entity_inputs, indent=2))
    print("rawInputs", json.dumps(raw_inputs, indent=2))
    print("Seeding complete")
