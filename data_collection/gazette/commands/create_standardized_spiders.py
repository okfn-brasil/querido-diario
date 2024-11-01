import csv
import re
from datetime import datetime
from urllib.parse import urlparse, urlunparse

from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode

source_file = r"../resources/cities_mapped.csv"
templates_dir = r"../../templates/standardized_spiders"
output_dir = r"../spiders/"


def read(file_path):
    data = []

    with open(file_path, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def write(output, filename):
    with open(f"{output_dir}/{filename}.py", "w") as f:
        print(output, file=f)


def _make_class_name(state, city):
    state = unidecode(state).strip().lower().capitalize()
    city = unidecode(city).strip().lower().replace("-", " ").replace("'", "")
    city_substrings = [x.capitalize() for x in city.split()]

    return f"{state}{''.join(city_substrings)}"


def _make_spider_name(state, city):
    state = unidecode(state).strip().lower()
    city = unidecode(city).strip().lower().replace("-", " ").replace("'", "")
    spider_name = f"{state}_{city.replace(' ', '_')}"

    return spider_name


def _format_date(rawdata):
    return (
        datetime.strptime(rawdata, "%Y-%m-%d")
        .strftime("%Y, %m, %d")
        .replace(", 0", ", ")
    )


def _set_path(entry, render):
    return f'{entry["state"].lower()}/{render["spider_name"]}'


def _spider_common_attributes(entry):
    attributes = {
        "class_name": _make_class_name(entry["state"], entry["city"]),
        "territory_id": entry["territory_id"],
        "spider_name": _make_spider_name(entry["state"], entry["city"]),
        "date_from": _format_date(entry["date_from"]),
    }

    if entry["status"] == "descontinuado":
        attributes["spider_name"] = _make_spider_name(
            entry["state"], f"{entry['city']} {attributes['date_from'][:4]}"
        )
        attributes["date_to"] = _format_date(entry["date_to"])

    return attributes


def create_spiders(data):
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)

    for entry in data:
        attributes = _spider_common_attributes(entry)

        match entry["pattern"]:
            case "adiarios_v1":
                template = env.get_template("adiarios_v1.jinja")
                render = set_adiarios_v1(entry, attributes)
            # case "adiarios_v2":
            # case "adiarios_v3":
            case "doem":
                template = env.get_template("doem.jinja")
                render = set_doem(entry, attributes)

            # TENDE A CRESCER MUITO

        spider_content = template.render(**render)
        spider_path = _set_path(entry, render)

        if entry["status"] == "descontinuado":
            spider_content += f"\n    end_date = date({render['date_to']})"

        write(spider_content, spider_path)


def set_adiarios_v1(entry, attributes):
    parsed_url = urlparse(entry["url"])
    replacements = {"path": "", "params": "", "query": "", "fragment": ""}
    attributes["base_url"] = urlunparse(parsed_url._replace(**replacements))
    attributes["domain"] = parsed_url.netloc.replace("www.", "")
    return attributes


# def set_adiarios_v2(entry, attributes):
# def set_adiarios_v3(entry, attributes):
# TENDE A CRESCER MUITO


def set_doem(entry, attributes):
    parsed_url = urlparse(entry["url"])
    attributes["state_city_url_part"] = re.search(
        r"/(.+)/diarios", parsed_url.path
    ).group(1)
    return attributes


def main(status=None, pattern=None):
    # talvez um recurso que permita os comandos
    # status: ativo / descontinuado
    # padrão: doem, dosp, etc
    # seja bom. Por padrão cria todos, mas parcial tb é possível

    data = read(source_file)
    create_spiders(data)


if __name__ == "__main__":
    main()
