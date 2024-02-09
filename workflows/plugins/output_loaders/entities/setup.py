#!/usr/bin/env python3
from setuptools import setup

setup(
    name="entity-output-loaders",
    version="0.0.1",
    description="Output loaders for czid entities",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["sequencing_read"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["miniwdl"],
    reentry_register=True,
    entry_points={
        "czid.plugin.output_loader": [
            "sequencing_read = sequencing_read:SequencingReadOutputLoader",
        ],
    },
)
