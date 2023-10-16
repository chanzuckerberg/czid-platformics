#!/usr/bin/env python3
from setuptools import setup

setup(
    name="event-bus-redis",
    version="0.0.1",
    description="A redis event bus",
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
        "czid.plugin.event_bus": [
            "redis = event_bus_redis:EventBusRedis",
        ],
    },
)
