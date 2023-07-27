#!/usr/bin/env python3
from setuptools import setup

setup(
    name="workflow_runner-swipe",
    version="0.0.1",
    description="Runs WDL workflows on swipe",
    url="",
    project_urls={
        "Documentation": "",
        "Source Code": "",
        "Issue Tracker": ""
    },
    long_description="",
    long_description_content_type="text/markdown",
    author="Todd Morse",
    py_modules=["workflow_runner_swipe"],
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=["miniwdl"],
    reentry_register=True,
    entry_points={
        'czid.plugin.workflow_runner': [
            'swipe = workflow_runner_swipe:SwipeWorkflowRunner',
        ],
    }
)
