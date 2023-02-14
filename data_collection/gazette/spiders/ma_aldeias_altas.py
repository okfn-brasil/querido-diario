from datetime import date, datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaAldeiasAltasSpider(BaseGazetteSpider):

    name = "ma_aldeias_altas"
    allowed_domains = ["aldeiasaltas.ma.gov.br"]
    start_date = date(2017, 5, 3)
    url_base = "http://aldeiasaltas.ma.gov.br/diario-oficial?data={}"
    TERRITORY_ID = "2100303"

    def start_requests(self):
        days = rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date)
        for day in days:
            yield scrapy.Request(self.url_base.format(day.strftime("%Y-%m-%d")))

    def parse(self, response):
        gazettes = response.css("tr")
        for gazette in gazettes:
            gazette_url = gazette.css("a::attr(href)")
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
