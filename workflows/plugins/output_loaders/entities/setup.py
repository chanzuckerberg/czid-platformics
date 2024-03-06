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
    py_modules=[
        "consensus_genome_output",
        "bulk_download_output",
    ],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["miniwdl"],
    reentry_register=True,
    entry_points={
        "czid.plugin.output_loader": [
            "consensus_genome = consensus_genome_output:ConsensusGenomeOutputLoader",
            "bulk_download = bulk_download_output:BulkDownloadOutputLoader",
        ],
    },
)
