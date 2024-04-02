"""
Create db for `migrate.sh` script
"""

from settings import APISettings
from sqlalchemy_utils import create_database, database_exists


def create_db() -> None:
    settings = APISettings.model_validate({})
    db_uri = settings.SYNC_DB_URI
    if database_exists(db_uri):
        print("Database already exists!")

    else:
        print("Database does not exist, creating database")
        create_database(db_uri)
        print("Database created")


if __name__ == "__main__":
    create_db()
