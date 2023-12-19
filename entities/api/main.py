"""
Launch the GraphQL server.
"""

import uvicorn
from platformics.api.setup import get_app, get_strawberry_config

import strawberry
from api.mutations import Mutation
from api.queries import Query

# ------------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------------


# Define schema and test schema
def get_schema() -> strawberry.Schema:
    strawberry_config = get_strawberry_config()
    api_schema = strawberry.Schema(query=Query, mutation=Mutation, config=strawberry_config)
    return api_schema


# Only create the app object if we're *not* just about to run a server.
# Doing this work on import and then again when invoking the server confuses vscode's debugger.
if __name__ == "__main__":
    config = uvicorn.Config("api.main:app", host="0.0.0.0", port=8009, log_level="info")
    server = uvicorn.Server(config)
    server.run()
else:
    # Create and run app
    app = get_app(get_schema())
