from dateparser import parse

import datetime as dt
import ast

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgGovernadorValadares(BaseGazetteSpider):
    MUNICIPALITY_ID = "3127701"
    name = "mg_governador_valadares"
    allowed_domains = ["valadares.mg.gov.br"]
    start_urls = [
        "https://www.valadares.mg.gov.br/ajaxpro/diel_diel_lis,App_Web_eozglfst.ashx"
    ]
    current_page = 0
    page_size = 10

    def start_requests(self):
        for u in self.start_urls:
            yield self.make_request(u, self.current_page)

    def make_request(self, url, page):
        return scrapy.Request(
            url,
            callback=self.parse,
            method="POST",
            headers={"X-AjaxPro-Method": "GetDiario",},
            body={
                "Page": page,
                "cdCaderno": 1,
                "Size": self.page_size,
                "dtDiario_menor": None,
                "dtDiario_maior": None,
                "dsPalavraChave": "",
                "nuEdicao": -1,
            },
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
            # pelo que vi cdLocal é sempre 12
            url = "http://www.valadares.mg.gov.br/abrir_arquivo.aspx?cdLocal=12&arquivo={}{}".format(
                row[6], row[7]
            )
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power="executive",
                scraped_at=dt.datetime.utcnow(),
            )

        self.current_page += 1
        yield self.make_request(self.start_urls[0], self.current_page)
