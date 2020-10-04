import ast
import datetime as dt
import json
import re

from dateparser import parse
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgGovernadorValadares(BaseGazetteSpider):
    TERRITORY_ID = "3127701"
    name = "mg_governador_valadares"
    allowed_domains = ["valadares.mg.gov.br"]
    start_urls = [
        "https://www.valadares.mg.gov.br/ajaxpro/diel_diel_lis,App_Web_eozglfst.ashx"
    ]

    current_page = 0
    ITEMS_PER_PAGE = 10

    def start_requests(self):
        url = self.start_urls[0]
        yield self.make_request(url, self.current_page)

    def make_request(self, url, page):
        return scrapy.Request(
            url,
            method="POST",
            headers={"X-AjaxPro-Method": "GetDiario",},
            body=self.make_body(page),
            dont_filter=True,
        )

    def parse(self, response):

        body = response.body
        has_no_results = body == "null;/*".encode()
        if has_no_results:
            return
        # remove 'new Ajax.Web.DataTable(' .... ');/*' do body
        body = body[23:-4]
        # bytes para str
        body = body.decode("utf-8")
        # remove o new Date para converter a data em uma tupla
        body = body.replace("new Date", "")
        # transforma a resposta em uma lista
        rows = None
        try:
            rows = ast.literal_eval(body)
        except:
            self.logger.error("Error parsing body variable > %s", body)
            return

        for row in rows[1]:
            d = row[4]
            date = dt.date(d[0], d[1] + 1, d[2])

            url = "http://www.valadares.mg.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}".format(
                row[6], row[7]
            )
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                power="executive",
                scraped_at=dt.datetime.utcnow(),
            )

        self.current_page += 1
        yield self.make_request(self.start_urls[0], self.current_page)

    def make_body(self, page):
        return json.dumps(
            {
                "Page": page,
                "cdCaderno": 1,
                "Size": str(self.ITEMS_PER_PAGE),
                "dtDiario_menor": None,
                "dtDiario_maior": None,
                "dsPalavraChave": "",
                "nuEdicao": -1,
            }
        )
