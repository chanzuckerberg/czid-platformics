"""
CLI program to start a listener
"""
import asyncio

from api.config import load_event_bus
from api.loader.loader import LoaderDriver
from settings import APISettings
from platformics.database.connect import init_async_db

if __name__ == "__main__":
    print("Starting loader listener")
    settings = APISettings.model_validate({})
    app_db = init_async_db(settings.DB_URI)
    session = app_db.session()

    event_bus = load_event_bus(settings)
    loader = LoaderDriver(session, event_bus)

    # call main in it's own thread
    loop = asyncio.get_event_loop()
    task = loop.create_task(loader.main())
    loop.run_until_complete(task)
