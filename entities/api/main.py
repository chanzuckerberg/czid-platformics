"""
Launch the GraphQL server.
"""

from platformics.api.setup import get_app, get_strawberry_config

import strawberry
from api.mutations import Mutation
from api.queries import Query

strawberry_config = get_strawberry_config()
api_schema = strawberry.Schema(query=Query, mutation=Mutation, config=strawberry_config)

# Create app object.
app = get_app(api_schema)
