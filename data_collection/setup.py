# Automatically created by: shub deploy

from setuptools import find_packages, setup

setup(
    name="project",
    version="1.0",
    packages=find_packages(),
    package_data={
        "gazette": ["resources/*.json", "resources/*.csv"],
    },
    entry_points={"scrapy": ["settings = gazette.settings"]},
)
