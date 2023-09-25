from abc import ABC
import asyncio
from dataclasses import dataclass, field, fields
import os
from typing import Generic, Optional
import typing
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
}


@dataclass
class Entity(ABC):
    entity_id: Optional[UUID] = field(default_factory=lambda: None, init=False)
    version: Optional[Version] = field(default_factory=lambda: Version(0), init=False)

    def _mutation_name(self):
        return f"create{self.__class__.__name__}"

    def _fields(self):
        for field in fields(self):
            if field.name in ["entity_id", "version"]:
                continue
            yield field

    def gql_create_mutation(self):
        field_name_types = []
        for field in self._fields():
            if field.type.__name__ == "EntityReference":
                field_name_types.append((field.metadata["id_name"], "UUID"))
                continue
            field_name_types.append((_snake_to_camel(field.name), _type_name_to_graphql_type[field.type.__name__]))

        # field_name_types.append(("userId", "Int"))
        field_name_types.append(("collectionId", "Int"))

        type_signature = ", ".join([f"${field_name}: {field_type}!" for field_name, field_type in field_name_types])
        variable_signature = ", ".join([f"{field_name}: ${field_name}" for field_name, _ in field_name_types])
        return f"""
            mutation Create{self.__class__.__name__}({type_signature}) {'{'}
                {self._mutation_name()}({variable_signature}) {'{'}
                    id
                {'}'}
            {'}'}
        """

    def gql_variables(self):
        variables = {}
        for field in self._fields():
            if field.type.__name__ == "EntityReference":
                variables[field.metadata["id_name"]] = getattr(self, field.name).entity_id
                continue
            variables[_snake_to_camel(field.name)] = getattr(self, field.name)

        return variables

    def get_dependent_entities(self):
        for field in fields(self):
            if field.type.__name__ == "EntityReference":
                entity_ref: EntityReference = getattr(self, field.name)
                yield entity_ref

    async def create_if_not_exists(self, user_id: int, collection_id: int, client: Client):
        if self.entity_id:
            return

        dependent_entity_futures = []
        for entity_ref in self.get_dependent_entities():
            dependent_entity_futures.append(entity_ref.create_if_not_exists(user_id, collection_id, client))
        await asyncio.gather(*dependent_entity_futures)

        variables = self.gql_variables()
        # variables["userId"] = user_id
        variables["collectionId"] = collection_id
        response = await client.execute_async(gql(self.gql_create_mutation()), variable_values=variables)
        entity_id = response.get(self._mutation_name(), {}).get("id")
        self.entity_id = entity_id


@dataclass
class Sample(Entity):
    name: str
    location: str


T = typing.TypeVar("T", bound=Entity)


@dataclass
class EntityReference(Generic[T]):
    entity_id: Optional[UUID] = field(default_factory=lambda: None)
    entity: Optional[T] = field(default_factory=lambda: None)

    async def create_if_not_exists(self, user_id: int, collection_id: int, client: Client):
        if self.entity_id:
            return
        if self.entity is None:
            raise ValueError("EntityReference has no entity")
        await self.entity.create_if_not_exists(user_id, collection_id, client)
        self.entity_id = self.entity.entity_id

    def exists(self):
        return self.entity_id is not None

    async def load(self):
        pass


@dataclass
class SequencingRead(Entity):
    nucleotide: str
    sequence: str
    protocol: str
    sample: EntityReference[Sample] = field(metadata={"id_name": "sampleId"})


@dataclass
class Contig(Entity):
    sequence: str
    sequencing_read: Optional[EntityReference[SequencingRead]] = field(metadata={"id_name": "sequencingReadId"})


async def create_entities(user_id: int, collection_id: int, entities: list[Entity]):
    headers = {"Authorization": f"Bearer {ENTITY_SERVICE_AUTH_TOKEN}"}
    transport = AIOHTTPTransport(url=ENTITY_SERVICE_URL, headers=headers)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    futures = []
    for entity in entities:
        futures.append(entity.create_if_not_exists(user_id, collection_id, client))
    await asyncio.gather(*futures)
