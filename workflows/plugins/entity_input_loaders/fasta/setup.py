#!/usr/bin/env python3
from setuptools import setup

setup(
    name="entity-input-loader-fasta",
    version="0.0.1",
    description="Loads a fasta entity",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["loader_fasta"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["miniwdl"],
    reentry_register=True,
    entry_points={
        "czid.plugin.entity_input_loader": [
            "fasta = loader_fasta:FastaLoader",
        ],
    },
)
