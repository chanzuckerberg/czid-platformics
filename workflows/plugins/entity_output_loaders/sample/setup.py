#!/usr/bin/env python3
from setuptools import setup

setup(
    name="entity-output-loader-sample",
    version="0.0.1",
    description="Loads a sample entity",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["loader_sample"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["miniwdl"],
    reentry_register=True,
    entry_points={
        "czid.plugin.entity_output_loader": [
            "sample = loader_sample:SampleLoader",
        ],
    },
)
