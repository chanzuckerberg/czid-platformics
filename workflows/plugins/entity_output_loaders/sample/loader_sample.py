""" 
Sample loader plugin
"""

from typing import List, TypedDict
from plugins.plugin_types import EntityOutputLoader
from entity_interface import Sample


class Input(TypedDict):
    name: str
    location: str


class SampleLoader(EntityOutputLoader):
    async def load(self, args: Input) -> List[Sample]:
        return [Sample(args["name"], args["location"])]
