"""
CLI program to start a listener
"""
import asyncio

from api.config import load_event_bus
from api.loader.loader import LoaderDriver
from settings import APISettings
from platformics.database.connect import init_async_db
import threading
import http.server
import socketserver
from http import HTTPStatus

PORT = 8000


def health_check() -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(b"Hello world")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


if __name__ == "__main__":
    print("Starting loader listener")
    settings = APISettings.model_validate({})
    app_db = init_async_db(settings.DB_URI)
    session = app_db.session()

    event_bus = load_event_bus(settings)
    loader = LoaderDriver(session, event_bus)

    # call main in it's own thread
    loop = asyncio.get_event_loop()

    # start server for health check
    t = threading.Thread(target=health_check)
    t.start()

    task = loop.create_task(loader.main())
    loop.run_until_complete(task)
