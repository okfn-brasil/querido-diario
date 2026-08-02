import json
from importlib.resources import files

GAZETTE_SCHEMA = json.loads(
    files("gazette")
    .joinpath("resources/gazette_schema.json")
    .read_text(encoding="utf-8")
)
