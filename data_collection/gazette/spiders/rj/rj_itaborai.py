from datetime import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjItaboraiSpider(BaseGazetteSpider):
    name = "rj_itaborai"
    TERRITORY_ID = "3301900"
    allowed_domains = ["do.ib.itaborai.rj.gov.br"]
    start_date = dt(2019, 1, 23).date()

    def start_requests(self):
        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")
        yield scrapy.FormRequest(
            url="https://do.ib.itaborai.rj.gov.br/dados-portal-novo.php",
            formdata={"acao": "3", "dado[]": [start_date, end_date]},
        )

    def parse(self, response):
        gazettes = response.xpath('//div[contains(@class, "card-avulso-diario")]')

        for gazette in gazettes:
            raw_gazette_date = gazette.xpath(
                './/p[contains(text(),"Postado em")]/text()'
            ).re_first(r"\d{2}/\d{2}/\d{4}")

            gazette_date = dt.strptime(raw_gazette_date, "%d/%m/%Y").date()

            gazette_edition_number = gazette.xpath(
                './/p[contains(text(),"Edição N°")]/text()'
            ).re_first(r"\d+")

            is_extra = "extra" in gazette.xpath("@class").get()

            gazette_url = gazette.xpath(".//a/@href").get()

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra,
                file_urls=[gazette_url],
                power="executive",
            )
