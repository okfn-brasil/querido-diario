from datetime import date

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrMaringaSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True
    TERRITORY_ID = "4115200"
    name = "pr_maringa"
    allowed_domains = ["maringa.pr.gov.br"]
    start_date = date(2007, 1, 1)

    def start_requests(self):
        yield scrapy.FormRequest(
            "https://venus.maringa.pr.gov.br/arquivos/orgao_oficial/seleciona_ano_oom.php",
            callback=self.parse_form,
        )

    def parse_form(self, response):
        for year in range(self.start_date.year, self.end_date.year + 1):
            yield scrapy.FormRequest.from_response(
                response,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                formnumber=0,
                formdata={"ano": str(year), "entrar": "Buscar"},
                callback=self.parse_year,
            )

    def parse_year(self, response):
        rows = response.css("table tr")[3:]
        for row in rows:
            gazette_file_link = row.css("td:nth-child(1) a::attr(href)").get()
            gazette_date = row.css("td:nth-child(2) font > font::text").get()
            data = parse(gazette_date, languages=["pt"]).date()
            edition = row.css("td:nth-child(1) a::text").re_first(r"\d+")
            if self.start_date <= data <= self.end_date:
                yield Gazette(
                    date=data,
                    edition_number=edition,
                    file_urls=[gazette_file_link],
                    is_extra_edition=False,
                    power="executive_legislative",
                )
