from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import daily_sequence


class MaAldeiasAltasSpider(BaseGazetteSpider):
    name = "ma_aldeias_altas"
    allowed_domains = ["aldeiasaltas.ma.gov.br"]
    start_date = date(2017, 5, 3)
    TERRITORY_ID = "2100303"

    def start_requests(self):
        for day in daily_sequence(self.start_date, self.end_date, format="%Y-%m-%d"):
            yield scrapy.Request(
                f"https://aldeiasaltas.ma.gov.br/diario-oficial?data={day}"
            )

    def parse(self, response):
        gazettes = response.css("tbody tr")
        for gazette in gazettes:
            gazette_url = gazette.css("a::attr(href)").get()
            gazette_date = datetime.strptime(
                gazette.xpath("td[2]/text()").get(), "%d/%m/%Y"
            )
            edition_number = gazette.xpath("td[1]/text()").re_first(r"\d+\/\d+|\d+")

            yield Gazette(
                date=gazette_date.date(),
                file_urls=[
                    gazette_url,
                ],
                edition_number=edition_number,
                power="executive",
            )
