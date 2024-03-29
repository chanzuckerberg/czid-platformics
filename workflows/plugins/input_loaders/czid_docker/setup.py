#!/usr/bin/env python3
from setuptools import setup

setup(
    name="czid-docker",
    version="0.0.1",
    description="Input loaders for czid docker image naming convention",
    url="",
    project_urls={"Documentation": "", "Source Code": "", "Issue Tracker": ""},
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["czid_docker"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["boto3"],
    reentry_register=True,
    entry_points={
        "czid.plugin.input_loader": [
            "czid_docker = czid_docker:CZIDDockerInputLoader",
        ],
    },
)
