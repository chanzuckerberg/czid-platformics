from abc import ABC
import asyncio
from dataclasses import dataclass, field, fields
import os
from typing import List, Optional
from uuid import UUID

from semver import Version
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


ENTITY_SERVICE_URL = os.environ["ENTITY_SERVICE_URL"]
ENTITY_SERVICE_AUTH_TOKEN = os.environ["ENTITY_SERVICE_AUTH_TOKEN"]


def _snake_to_camel(s: str):
    title = "".join(word.title() for word in s.split("_"))
    return title[0].lower() + title[1:]


_type_name_to_graphql_type = {
    "str": "String",
    "int": "Int",
    "float": "Float",
    "bool": "Boolean",
    "UUID": "ID",
}

@dataclass
class Entity(ABC):
    entity_id: Optional[UUID] = field(default_factory=lambda: None, init=False)
    version: Optional[Version] = field(default_factory=lambda: Version(0), init=False)

    def _mutation_name(self):
        return f"create{self.__class__.__name__}"

    def gql_create_mutation(self):
        field_name_types = []
        for field in fields(self):
            if field.name in ["entity_id", "version"]:
                continue
            field_name_types.append((_snake_to_camel(field.name), _type_name_to_graphql_type[field.type.__name__]))

        # field_name_types.append(("userId", "Int"))
        field_name_types.append(("collectionId", "Int"))

        type_signature = ", ".join([f"${field_name}: {field_type}!" for field_name, field_type in field_name_types])
        variable_signature = ", ".join([f"{field_name}: ${field_name}" for field_name, _ in field_name_types])
        return f"""
            mutation Create{self.__class__.__name__}({type_signature}) {'{'}
                {self._mutation_name()}({variable_signature}) {'{'}
                    entityId
                {'}'}
            {'}'}
        """

    def gql_variables(self):
        variables = {}
        for field in fields(self):
            if field.name in ["entity_id", "version"]:
                continue
            variables[_snake_to_camel(field.name)] = getattr(self, field.name)

        return variables
    
    async def create(self, user_id: int, collection_id: int, client: Client):
        if self.entity_id is not None:
            raise ValueError("Entity already has an entity_id")

        variables = self.gql_variables()
        # variables["userId"] = user_id
        variables["collectionId"] = collection_id
        response = await client.execute_async(gql(self.gql_create_mutation()), variable_values=variables)
        entity_id = response.get(self._mutation_name(), {}).get("entity_id")
        self.entity_id = entity_id


@dataclass
class Sample(Entity):
    name: str
    location: str


@dataclass
class SequencingRead(Entity):
    nucleotide: str
    sequence: str
    protocol: str
    sample_id: Optional[UUID] = field(default_factory=lambda: None)


@dataclass
class Contig(Entity):
    sequence: str
    sequencing_read_id: Optional[UUID] = field(default_factory=lambda: None)



async def create_entities(user_id: int, collection_id: int, entities: List[List[Entity]]):
    headers = {"Authorization": f"Bearer {ENTITY_SERVICE_AUTH_TOKEN}"}
    transport = AIOHTTPTransport(url=ENTITY_SERVICE_URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    for entity_list in entities:
        futures = []
        for entity in entity_list:
            futures.append(entity.create(user_id, collection_id, client))
        await asyncio.gather(*futures)
