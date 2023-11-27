#!/usr/bin/env python3
from setuptools import setup

setup(
    name="czid-entity-loaders",
    version="0.0.1",
    description="Suite of loaders to load CZID entities",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["reference_genome", "sample", "sequencing_read", "consensus_genome"],
    python_requires=">=3.6",
    setup_requires=[],
    reentry_register=True,
    entry_points={
        "czid.plugin.entity_input_loader": [
            "reference_genome = reference_genome:ReferenceGenomeInputLoader",
            "sample = sample:SampleInputLoader",
            "sequencing_read = sequencing_read:SequencingReadInputLoader",
        ],
        "czid.plugin.entity_output_loader": [
            "consensus_genome = consensus_genome:ConsensusGenomeLoader",
        ],
    },
)
