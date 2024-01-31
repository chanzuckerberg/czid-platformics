"""
Make sure deleted entities are not returned by the API.
"""

import time
import datetime
import pytest
import sqlalchemy as sa
from database.models import File
from platformics.database.connect import SyncDB
from platformics.codegen.conftest import GQLTestClient, SessionStorage, FileFactory
from platformics.codegen.tests.output.test_infra.factories.sample import SampleFactory
from platformics.codegen.tests.output.test_infra.factories.sequencing_read import SequencingReadFactory


@pytest.mark.asyncio
async def test_deleted_at(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    """
    Make sure deleted entities aren't returned by the API.
    """
    user_id = 12345
    project_id = 123
    date_now = datetime.datetime.now()

    # Create mock data
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        params = {
            "collection_location": "Mountain View, CA",
            "collection_date": date_now,
            "owner_user_id": user_id,
            "collection_id": project_id,
        }
        # Create samples that are not deleted, deleted, and deleted in the future
        SampleFactory.create_batch(5, **params)
        SampleFactory.create_batch(5, **params, deleted_at=date_now)
        SampleFactory.create_batch(5, **params, deleted_at=date_now + datetime.timedelta(seconds=2))

    # Fetch all samples
    query = """
        query MyQuery {
            samples {
                id
            }
        }
    """

    # At first, expect 10 samples
    output = await gql_client.query(query, user_id=user_id, member_projects=[project_id])
    assert len(output["data"]["samples"]) == 10

    # After a few seconds, 5 of the samples should not show up anymore
    time.sleep(3)
    output = await gql_client.query(query, user_id=user_id, member_projects=[project_id])
    assert len(output["data"]["samples"]) == 5

@pytest.mark.asyncio
async def test_deleted_at_aggregate(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    """
    Make sure deleted entities aren't returned by the API in aggregate queries.
    """
    user_id = 12345
    project_id = 123
    date_now = datetime.datetime.now()

    # Create mock data
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        params = {
            "collection_location": "Mountain View, CA",
            "collection_date": date_now,
            "owner_user_id": user_id,
            "collection_id": project_id,
        }
        # Create samples that are not deleted, deleted, and deleted in the future
        SampleFactory.create_batch(5, **params)
        SampleFactory.create_batch(5, **params, deleted_at=date_now)
        SampleFactory.create_batch(5, **params, deleted_at=date_now + datetime.timedelta(seconds=2))

    # Fetch all samples
    query = """
        query MyQuery {
            samplesAggregate {
                aggregate {
                    count
                }
            }
        }
    """

    # At first, expect 10 samples
    output = await gql_client.query(query, user_id=user_id, member_projects=[project_id])
    assert output["data"]["samplesAggregate"]["aggregate"]["count"] == 10

    # After a few seconds, 5 of the samples should not show up anymore
    time.sleep(3)
    output = await gql_client.query(query, user_id=user_id, member_projects=[project_id])
    assert output["data"]["samplesAggregate"]["aggregate"]["count"] == 5

@pytest.mark.asyncio
async def test_deleted_at_files(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    """
    Make sure deleted files aren't returned by the API.
    """
    user_id = 12345
    project_id = 123

    # Create mock data and mark 1 of the files as deleted
    with sync_db.session() as session:
        SessionStorage.set_session(session)
        SequencingReadFactory.create(owner_user_id=user_id, collection_id=project_id)
        FileFactory.update_file_ids()
        session.commit()
        files = session.execute(sa.select(File)).scalars().all()
        files[0].deleted_at = datetime.datetime.now()
        session.commit()

    # Fetch all samples
    query = """
        query MyQuery {
            files {
                id
            }
        }
    """

    # Should not return the 1 file that was deleted
    output = await gql_client.query(query, user_id=user_id, member_projects=[project_id])
    assert len([f for f in output["data"]["files"] if f["id"] == files[0].id]) == 0
