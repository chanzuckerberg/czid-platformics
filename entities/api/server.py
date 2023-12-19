"""
Launch the GraphQL server.
"""

import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config("api.main:app", host="0.0.0.0", port=8009, log_level="info")
    server = uvicorn.Server(config)
    server.run()
