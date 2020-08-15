from collections import defaultdict
import re
from pathlib import Path


def main():
    root = Path(__file__).parent
    spiders = root / "spiders"
    pattern = r"([a-z]{2})_([a-z_]+)\.py"

    results = defaultdict(list)

    for f in spiders.glob("*.py"):
        name = f.name
        matches = re.findall(pattern, name)

        if matches:
            state, city = matches[0]
            city = city.replace("_", " ").title()
            results[state].append(city)

    print(results)


if __name__ == "__main__":
    main()
