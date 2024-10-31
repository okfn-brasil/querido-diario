import csv
import re
from datetime import datetime
from urllib.parse import urlparse, urlunparse

from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode


class SpiderFileMaker:
    OUTPUT_DIR = r"../spiders"
    TEMPLATES_DIR = r"../../templates/standardized_spiders"

    entry = None
    attributes = None
    template_file = None

    def __init__(self, entry):
        entry["state"] = self._sanitize(entry["state"])
        entry["city"] = self._sanitize(entry["city"])

        self.entry = entry
        self.set_spider_basic_attributes()
        self.add_spider_specific_attributes()
        self.write_spider()

    def set_spider_basic_attributes(self):
        if self.entry["status"] == "descontinuado":
            self.entry["city"] = f"{self.entry['city']} {self.entry['date_from'][:4]}"

        self.attributes = {
            "class_name": self._make_class_name(),
            "territory_id": self.entry["territory_id"],
            "spider_name": self._make_spider_name(),
            "date_from": self._format_date(),
        }

    def add_spider_specific_attributes(self):
        pattern = self.entry["pattern"]
        if pattern == "adiarios_v1":
            self.set_adiarios_v1()
        elif pattern == "doem":
            self.set_doem()

    def write_spider(self):
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIR), autoescape=True)

        template = env.get_template(self.template_file)
        spider_content = template.render(**self.attributes)

        with open(self._make_filepath(), "w") as f:
            print(spider_content, file=f)

    def set_adiarios_v1(self):
        self.template_file = "adiarios_v1.jinja"

        parsed_url = urlparse(self.entry["url"])
        replacements = {"path": "", "params": "", "query": "", "fragment": ""}
        self.attributes["base_url"] = urlunparse(parsed_url._replace(**replacements))
        self.attributes["domain"] = parsed_url.netloc.replace("www.", "")

    def set_doem(self):
        self.template_file = "doem.jinja"

        parsed_url = urlparse(self.entry["url"])
        self.attributes["state_city_url_part"] = re.search(
            r"/(.+)/diarios", parsed_url.path
        ).group(1)

    def _sanitize(self, text):
        return unidecode(text).strip().lower().replace("-", " ").replace("'", "")

    def _make_class_name(self):
        state = self.entry["state"].capitalize()
        city_substrings = [x.capitalize() for x in self.entry["city"].split()]
        return f"{state}{''.join(city_substrings)}"

    def _make_spider_name(self):
        return f"{self.entry['state']}_{self.entry['city'].replace(' ', '_')}"

    def _format_date(self):
        return (
            datetime.strptime(self.entry["date_from"], "%Y-%m-%d")
            .strftime("%Y, %m, %d")
            .replace(", 0", ", ")
        )

    def _make_filepath(self):
        file_name = self.attributes["spider_name"]
        return f'{self.OUTPUT_DIR}/{self.entry["state"]}/{file_name}.py'


source_file = r"../resources/cidades_mapeadas.csv"
with open(source_file, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        SpiderFileMaker(row)
