#!/usr/bin/env python3
from setuptools import setup

setup(
    name="czid-workflows",
    version="0.0.1",
    description="Input loaders for czid workflows",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["consensus_gneome"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["miniwdl"],
    reentry_register=True,
    entry_points={
        "czid.plugin.input_loader": [
            "consensus_genome = consensus_genome:ConsensusGenomeInputLoader",
        ],
    },
)
