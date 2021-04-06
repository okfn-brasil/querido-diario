import ast
import json
import re
from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgGovernadorValadares(BaseGazetteSpider):
    TERRITORY_ID = "3127701"
    name = "mg_governador_valadares"
    allowed_domains = ["valadares.mg.gov.br"]
    start_urls = [
        "https://www.valadares.mg.gov.br/diario-eletronico/caderno/diario-oficial-eletronico/1"
    ]

    ITEMS_PER_PAGE = "100"
    BASE_URL = "https://www.valadares.mg.gov.br/"

    path = ""
    current_page = 0

    def parse(self, response):
        self.path = self.get_path_to_request_items(response)
        yield self.make_request(self.current_page)

    def get_path_to_request_items(self, response):
        scripts = response.xpath("//script//@src").extract()
        endpoint = next(path for path in scripts if "diel_diel_lis" in path)
        return endpoint

    def parse_items(self, response):
        body = response.body

        if self.is_body_empty(body):
            return

        definition, rows = self.parse_definitions_and_rows(body)

        for row in rows:
            item = dict(zip(definition, row))

            date_values = item["DTPUBLICACAO"]
            item_date = date(date_values[0], date_values[1] + 1, date_values[2])

            url = "https://www.valadares.mg.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}".format(
                item["NMARQUIVO"], item["NMEXTENSAOARQUIVO"]
            )
            yield Gazette(
                date=item_date,
                file_urls=[url],
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                power="executive",
                scraped_at=datetime.utcnow(),
            )

        self.current_page += 1
        yield self.make_request(self.current_page)

    def make_request(self, page):
        return scrapy.Request(
            f"{self.BASE_URL}{self.path}",
            method="POST",
            headers={
                "X-AjaxPro-Method": "GetDiario",
            },
            body=self.make_body(page),
            callback=self.parse_items,
        )

    def make_body(self, page):
        return json.dumps(
            {
                "Page": page,
                "cdCaderno": 1,
                "Size": self.ITEMS_PER_PAGE,
                "dtDiario_menor": self.parse_start_date(),
                "dtDiario_maior": None,
                "dsPalavraChave": "",
                "nuEdicao": -1,
            }
        )

    def parse_start_date(self):
        if not hasattr(self, "start_date"):
            return None

        return {
            "__type": "System.DateTime",
            "Year": self.start_date.year,
            "Month": self.start_date.month,
            "Day": self.start_date.day,
            "Hour": 0,
            "Millisecond": 0,
            "Minute": 0,
            "Second": 0,
        }

    def is_body_empty(self, body):
        return body == "null;/*".encode()

    def parse_definitions_and_rows(self, body):
        content = self.extract_items_data(body)

        definition, rows = [], []

        try:
            definition, rows = ast.literal_eval(content)
            definition = [name for name, property_type in definition]
        except Exception:
            return [], []

        return definition, rows

    def extract_items_data(self, body):
        content = re.findall(
            r"new Ajax\.Web\.DataTable\((?P<conteudo>.*)\);", body.decode("utf-8")
        )[0]
        content = content.replace("new Date", "")

        return content
