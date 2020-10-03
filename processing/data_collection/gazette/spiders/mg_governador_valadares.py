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
        "http://www.valadares.mg.gov.br/ajaxpro/diel_diel_lis,App_Web_diel_diel_lis.aspx.cdcab7d2.tw0oogts.ashx"
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
            headers={
                "Content-Type": "text/plain",
                "X-AjaxPro-Method": "GetDiario",
                "Referer": "http://www.valadares.mg.gov.br/diario-eletronico/caderno/diario-oficial-eletronico/1",
                "Origin": "http://www.valadares.mg.gov.br",
                "Host": "www.valadares.mg.gov.br",
            },
            body='{"Page":%s,"cdCaderno":1,"Size":%s,"dtDiario_menor":null,"dtDiario_maior":null,"dsPalavraChave":"","nuEdicao":-1}'
            % (page, self.page_size),
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
            url = "http://www.valadares.mg.gov.br/abrir_arquivo.aspx?cdLocal={}&arquivo={}{}".format(
                12, row[6], row[7]
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
