from collections import defaultdict
from os import stat
import re
from pathlib import Path


def list_spiders(path="spiders"):
    """
    Lists all the spiders available and breaks their names
    in state and city.

    Returns a dictionary containing the state's initials
    and a list of its cities.
    """
    root = Path(__file__).parent
    spiders = root / "spiders"
    pattern = r"^([a-z]{2})_([a-z_]+)\.py$"

    results = defaultdict(list)

    for f in spiders.glob("*.py"):
        name = f.name
        matches = re.findall(pattern, name)

        if matches:
            state, city = matches[0]
            state = state.upper()
            city = city.replace("_", " ").title()
            results[state].append(city)

    return results


def print_spiders_list(spider_list):
    """
    Given a dictionary as returned by `lists_spiders`,
    prints them in a user-friendly format.

    Currently, it will order the keys alphabetically
    and print each city on a separate line, also
    alphabetically. At the end of each key, it
    prints a separator.
    """
    for state in sorted(spider_list.keys()):
        print(f"Cidades de {state}")
        for city in sorted(spider_list[state]):
            print(f"\t{city}")
        print("*-" * 20, "*", sep="")


def main():
    results = list_spiders()
    print_spiders_list(results)


if __name__ == "__main__":
    main()
