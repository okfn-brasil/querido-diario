from datetime import date
from urllib.parse import urlparse

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSaoPauloSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550308"
    name = "sp_sao_paulo"
    start_date = date(1899, 1, 10)
    allowed_domains = ["diariooficial.prefeitura.sp.gov.br"]
    start_urls = [
        "https://diariooficial.prefeitura.sp.gov.br/md_epubli_controlador.php?acao=memoria_listar"
    ]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 5,
    }

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
