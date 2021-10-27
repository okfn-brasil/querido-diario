from datetime import date, datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaAldeiasAltasSpider(BaseGazetteSpider):

    name = "ma_aldeias_altas"
    allowed_domains = ["aldeiasaltas.ma.gov.br"]
    start_date = date(2017, 5, 3)
    url_base = "http://aldeiasaltas.ma.gov.br/diario-oficial?data={}"  # 2017-05-03
    TERRITORY_ID = "2100303"

    def start_requests(self):
        days = rrule(freq=DAILY, dtstart=self.start_date, until=date.today())
        for day in days:
            yield scrapy.Request(self.url_base.format(day.strftime("%Y-%m-%d")))

    def parse(self, response):
        gazettes = response.xpath("//table/tbody/tr")
        gazettes.reverse()
        for gazette_number, gazette in enumerate(gazettes):
            file_url = gazette.xpath("td[4]/a/@href").get()
            if not (file_url):
                continue
            edition_info = gazette.xpath("td[1]/text()")
            if edition_info.get() == "Não tem atos oficiais nesta data":
                continue
            gazette_date = datetime.strptime(
                gazette.xpath("td[2]/text()").get(), "%d/%m/%Y"
            )
            is_extra_edition = bool(gazette_number)
            edition_number = edition_info.re_first(r"\d+\/\d+|\d+")
            yield Gazette(
                date=gazette_date.date(),
                file_urls=[file_url],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power="executive",
                scraped_at=datetime.utcnow(),
            )
