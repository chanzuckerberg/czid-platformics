#!/usr/bin/env python3
from setuptools import setup

setup(
    name="entity-input-loaders",
    version="0.0.1",
    description="Input loaders for czid entities",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["entities"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["sgqlc"],
    reentry_register=True,
    entry_points={
        "czid.plugin.input_loader": [
            "sample = entities:SampleInputLoader",
            "sequencing_read = entities:SequencingReadInputLoader",
            "ncbi_index = entities:IndexFileInputLoader",
        ],
    },
)
