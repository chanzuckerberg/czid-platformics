"""
Make sure deleted entities are not returned by the API.
"""

import time
import datetime
import pytest
from platformics.database.connect import SyncDB
from platformics.codegen.conftest import GQLTestClient, SessionStorage
from platformics.codegen.tests.output.test_infra.factories.sample import SampleFactory


@pytest.mark.asyncio
async def test_deleted_at(
    sync_db: SyncDB,
    gql_client: GQLTestClient,
) -> None:
    """
    Make sure deleted entities don't show up
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
    Make sure deleted entities don't show up in aggregate queries either
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
