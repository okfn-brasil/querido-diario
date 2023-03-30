import csv
from functools import lru_cache

import pkg_resources


@lru_cache
def territories_metadata():
    territories_file = pkg_resources.resource_filename(
        "gazette", "resources/territories.csv"
    )
    with open(territories_file, encoding="utf-8") as csvfile:
        rows = [r for r in csv.DictReader(csvfile)]

    return rows
