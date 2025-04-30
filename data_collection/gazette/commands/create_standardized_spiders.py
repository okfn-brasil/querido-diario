import csv
import sys
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from patterns import PatternsSpecifcs
from text_unidecode import unidecode


class SpiderFileMaker:
    """Creates a spider file by filling a template placeholders with given website info

    Attributes:
        OUTPUT_DIR (str): directory path to save created spider file
        TEMPLATES_DIR (str): directory path where spider pattern templates are
        website_info (dict): website information, such as URL, publication dates, pattern, etc
    """

    OUTPUT_DIR = r"../spiders"
    TEMPLATES_DIR = r"../../templates/standardized_spiders"
    website_info = None

    def __init__(self, website_info):
        self.website_info = website_info
        self.website_info["state"] = self._sanitize(website_info["state"])
        self.website_info["city"] = self._sanitize(website_info["city"])
        self.create_spider()

    def create_spider(self):
        """Write a code file with website info expected in template fields

        Template fields have two types:
        1. General: fields that every spider must have, doesnt matter which
        pattern, because is demanded by project code style, such as spider name,
        territory_id, start date, etc
        2. Specific: fields that exists in a pattern only

        Example:
            In a hypothetical.jinja template, placeholder fields are:

                class {{ class_name }}Spider(BaseHypotheticalSpider):
                    TERRITORY_ID = "{{ territory_id }}"
                    name = "{{ spider_name }}"
                    start_date = date({{ date_from }})
                    allowed_domains = ["{{ domain }}"]
                    base_url = "{{ base_url }}"

            So, common_attributes() builds a dict with...
                {   'class_name': '...',
                    'territory_id': '...',
                    'spider_name': '...',
                    'date_from': '...',
                }
            and add_specific_attributes() completes it with ...
                {   'domain': '...',
                    'base_url': '...',
                }

            then, write_spider() fills template fields with dict data and save
            text to file
        """
        attributes = self.common_attributes()
        template_file, attributes = self.add_specific_attributes(attributes)
        self.write_spider(attributes, template_file)

    def common_attributes(self):
        """Sets spider general attributes"""

        if self.website_info["status"] == "descontinuado":
            self.website_info[
                "city"
            ] = f"{self.website_info['city']} {self.website_info['date_from'][:4]}"

        return {
            "class_name": self._make_class_name(),
            "territory_id": self.website_info["territory_id"],
            "spider_name": self._make_spider_name(),
            "date_from": self._format_date(self.website_info["date_from"]),
        }

    def add_specific_attributes(self, attributes):
        """Adds spider exclusive attributes"""

        pattern = self.website_info["pattern"]
        method = getattr(PatternsSpecifcs, pattern)
        return method(self.website_info, attributes)

    def write_spider(self, attributes, template_file):
        """Writes file, in spiders directory, with template placeholders filled
        with attributes"""

        env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIR), autoescape=True)
        template = env.get_template(template_file)
        spider_content = template.render(**attributes)
        spider_content = self._add_end_date(spider_content)

        with open(self._make_filepath(attributes), "w") as f:
            print(spider_content, file=f)

    def _sanitize(self, text):
        return unidecode(text).strip().lower().replace("-", " ").replace("'", "")

    def _make_class_name(self):
        state = self.website_info["state"].capitalize()
        city_substrings = [x.capitalize() for x in self.website_info["city"].split()]
        return f"{state}{''.join(city_substrings)}"

    def _make_spider_name(self):
        return f"{self.website_info['state']}_{self.website_info['city'].replace(' ', '_')}"

    def _make_filepath(self, attributes):
        file_name = attributes["spider_name"]
        return f'{self.OUTPUT_DIR}/{self.website_info["state"]}/{file_name}.py'

    def _format_date(self, date):
        if self.website_info["date_from"] == "Edição com data ausente":
            return ") # verificar manualmente"

        return (
            datetime.strptime(date, "%Y-%m-%d")
            .strftime("%Y, %m, %d")
            .replace(", 0", ", ")
        )

    def _add_end_date(self, spider_content):
        if self.website_info["status"] == "descontinuado":
            end_date = self._format_date(self.website_info["date_to"])
            new_line = f"\n    end_date = date({end_date})"
            spider_content += new_line
        return spider_content


# this script can be used in two ways:

# without args: creates all patterns spiders
# >>> python3 create_standardized_spiders.py

# with args: creates a specific pattern spiders
# >>> python3 create_standardized_spiders.py doem instar

patterns_to_create_spiders = sys.argv[1:]
source_file = r"../resources/cidades_mapeadas.csv"
with open(source_file, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if len(sys.argv[1:]) == 0:
            SpiderFileMaker(row)
        else:
            if row["pattern"] in patterns_to_create_spiders:
                SpiderFileMaker(row)
