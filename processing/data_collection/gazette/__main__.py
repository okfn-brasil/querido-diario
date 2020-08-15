from collections import defaultdict
from os import stat
import re
from pathlib import Path


def main():
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

    for state in sorted(results.keys()):
        print(f"Cidades de {state}")
        for city in sorted(results[state]):
            print(f"\t{city}")
        print("*-" * 20, "*", sep="")


if __name__ == "__main__":
    main()
