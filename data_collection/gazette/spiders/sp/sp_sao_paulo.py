import random
from datetime import date
from urllib.parse import urlparse

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoPauloSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550308"
    name = "sp_sao_paulo"
    start_date = date(2017, 6, 1)  # pra lá de 1900
    allowed_domains = ["diariooficial.prefeitura.sp.gov.br"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 10,
    }

    def start_requests(self):
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
        ]

        headers = {
            "User-Agent": user_agent_list[random.randint(0, len(user_agent_list) - 1)],
        }

        yield scrapy.Request(
            "https://diariooficial.prefeitura.sp.gov.br/md_epubli_controlador.php?acao=memoria_listar",
            headers=headers,
        )

    def parse(self, response):
        for year_option in response.css(".mandato-ano"):
            year = int(year_option.css("::text").get())
            year_formkey = year_option.attrib["data-value"]

            if self.start_date.year <= year <= self.end_date.year:
                for month in range(1, 13):
                    if (
                        self.start_date
                        <= date(year, month, self.start_date.day)
                        <= self.end_date
                    ):
                        yield scrapy.FormRequest.from_response(
                            response,
                            formdata={
                                "hdnFiltroMandato": year_formkey,
                                "hdnFiltroMes": str(month),
                            },
                            callback=self.parse_editions,
                        )

    def parse_editions(self, response):
        for item in response.css(".painelEdições.clearfix a"):
            gazette_url = item.attrib["href"]
            gazette_url = urlparse(gazette_url)._replace(scheme="https").geturl()
            raw_date = "/".join(item.css(".legenda h3::text").getall())
            edition_date = parse(raw_date, languages=["pt"]).date()

            if self.start_date <= edition_date <= self.end_date:
                yield Gazette(
                    date=edition_date,
                    file_urls=[gazette_url],
                    edition_number="",
                    is_extra_edition=False,
                    power="executive",
                )
