#!/usr/bin/env python3
from setuptools import setup

from sample import entity_input_loaders

setup(
    name="entity-input-loaders",
    version="0.0.1",
    description="Input loaders for czid entities",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["event_bus_redis"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["miniwdl"],
    reentry_register=True,
    entry_points={
        "czid.plugin.input_loader": [
            f"{entity_type} = sample:entity_input_loaders['{entity_type}']" for entity_type in entity_input_loaders
        ],
    },
)
