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


_type_name_to_graphql_type = {
    "str": "String",
    "int": "Int",
    "float": "Float",
    "bool": "Boolean",
    "UUID": "ID",
}

def _title_to_snake_case(string: str):
    return "".join(["_" + char.lower() if char.isupper() else char for char in string]).lstrip("_")

@dataclass
class Entity(ABC):
    entity_id: Optional[UUID] = field(default_factory=lambda: None, init=False)
    version: Optional[Version] = field(default_factory=lambda: Version(0), init=False)

    def _mutation_name(self):
        return f"create_{_title_to_snake_case(self.__class__.__name__)}"

    def gql_create_mutation(self):
        field_name_types = []
        for field in fields(self):
            if field.name in ["entity_id", "version"]:
                continue
            field_name_types.append((field.name, _type_name_to_graphql_type[field.type.__name__]))

        type_signature = ", ".join([f"${field_name}: {field_type}!" for field_name, field_type in field_name_types])
        variable_signature = ", ".join([f"{field_name}: ${field_name}" for field_name, _ in field_name_types])
        mutation_name = f"create_{_title_to_snake_case(self.__class__.__name__)}"
        return f"""
            mutation Create{self.__class__.__name__}({type_signature}) {'{'}
                {mutation_name}({variable_signature}) {'{'}
                    entity_id
                {'}'}
            {'}'}
        """

    def gql_variables(self):
        variables = {}
        for field in fields(self):
            if field.name in ["entity_id", "version"]:
                continue
            variables[field.name] = getattr(self, field.name)

        return variables
    
    async def create(self, client: Client):
        if self.entity_id is not None:
            raise ValueError("Entity already has an entity_id")

        response = await client.execute_async(gql(self.gql_create_mutation()), variable_values=self.gql_variables())
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



async def create_entities(entities: List[List[Entity]]):
    headers = {"Authorization": f"Bearer {ENTITY_SERVICE_AUTH_TOKEN}"}
    transport = AIOHTTPTransport(url=ENTITY_SERVICE_URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    for entity_list in entities:
        futures = []
        for entity in entity_list:
            futures.append(entity.create(client))
        await asyncio.gather(*futures)
