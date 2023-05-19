import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrMaringaSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True
    name = "pr_maringa"
    TERRITORY_ID = "4115200"
    start_date = datetime.date(2007, 1, 5)
    allowed_domains = ["maringa.pr.gov.br"]
    start_urls = [
        "https://venus.maringa.pr.gov.br/arquivos/orgao_oficial/seleciona_ano_oom.php"
    ]

    def parse(self, response):
        for year in range(self.start_date.year, self.end_date.year + 1):
            yield scrapy.FormRequest.from_response(
                response,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                formnumber=0,
                formdata={"ano": str(year), "entrar": "Buscar"},
                callback=self.parse_year,
            )
        yield from self.parse_year(response)

    def parse_year(self, response):
        rows = response.css("table tr")[3:]
        for row in rows:
            gazette_date = row.css("td:nth-child(2) font > font::text").get().strip()
            gazette_date = datetime.datetime.strptime(gazette_date, "%d/%m/%Y").date()

            if self.start_date <= gazette_date <= self.end_date:
                gazette_link = row.css("td:nth-child(1) a::attr(href)").get()
                edition = row.css("td:nth-child(1) a::text").get()[1:]

                yield Gazette(
                    date=gazette_date,
                    edition_number=edition,
                    file_urls=[gazette_link],
                    is_extra_edition=False,
                    power="executive_legislative",
                )
