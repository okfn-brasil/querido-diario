import ast
from datetime import datetime, date
import json
import re

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
        scripts = response.xpath("//script//@src").extract()
        endpoint = next(path for path in scripts if "diel_diel_lis" in path)
        self.path = endpoint
        yield self.make_request(self.current_page)

    def parse_items(self, response):
        body = response.body
        has_no_results = body == "null;/*".encode()
        if has_no_results:
            return

        content = re.findall(
            "new Ajax\.Web\.DataTable\((?P<conteudo>.*)\);", body.decode("utf-8")
        )[0]
        content = content.replace("new Date", "")

        rows = None
        definition = None

        try:
            definition, rows = self.extract_definitions_and_rows(content)
        except Exception as e:
            return

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

    def make_body(self, page):
        return json.dumps(
            {
                "Page": page,
                "cdCaderno": 1,
                "Size": self.ITEMS_PER_PAGE,
                "dtDiario_menor": None,
                "dtDiario_maior": None,
                "dsPalavraChave": "",
                "nuEdicao": -1,
            }
        )

    def extract_definitions_and_rows(self, content):
        definition, rows = ast.literal_eval(content)
        definition = [name for name, property_type in definition]

        return definition, rows

    def make_request(self, page):
        return scrapy.Request(
            f"{self.BASE_URL}{self.path}",
            method="POST",
            headers={"X-AjaxPro-Method": "GetDiario",},
            body=self.make_body(page),
            callback=self.parse_items,
        )
