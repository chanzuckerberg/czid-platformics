"""
Creates the database if it does not exist. Used by migrate.sh script.
"""

from platformics.settings import APISettings
from sqlalchemy_utils import create_database, database_exists


def create_db() -> None:
    """
    Creates the database
    """
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
