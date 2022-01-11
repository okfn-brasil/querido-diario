from datetime import date

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrMaringaSpider(BaseGazetteSpider):
    TERRITORY_ID = "4115200"
    name = "pr_maringa"
    allowed_domains = ["maringa.pr.gov.br"]

    def start_requests(self):
        """
        @url http://venus.maringa.pr.gov.br/arquivos/orgao_oficial/seleciona_ano_oom.php
        @returns requests 1
        """
        yield scrapy.FormRequest(
            "http://venus.maringa.pr.gov.br/arquivos/orgao_oficial/seleciona_ano_oom.php",
            callback=self.parse_form,
        )

    def parse_form(self, response):
        todays_date = date.today()
        current_year = todays_date.year
        for year in range(current_year, 2006, -1):
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
            gazette_file_link = row.css("td:nth-child(1) a::attr(href)").extract_first()
            gazette_date = row.css("td:nth-child(2) font > font::text").extract_first()
            yield Gazette(
                date=parse(gazette_date, languages=["pt"]).date(),
                file_urls=[gazette_file_link],
                is_extra_edition=any(
                    caracter.isalpha() for caracter in gazette_file_link.split(" ")[-1]
                ),
                power="executive_legislative",
            )
