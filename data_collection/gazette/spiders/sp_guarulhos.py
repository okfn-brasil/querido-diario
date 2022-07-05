import datetime as dt

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpGuarulhosSpider(BaseGazetteSpider):
    TERRITORY_ID = "3518800"
    name = "sp_guarulhos"
    allowed_domains = ["diariooficial.guarulhos.sp.gov.br"]
    start_date = dt.date(2015, 1, 1)

    BASE_URL = "https://diariooficial.guarulhos.sp.gov.br/index.php"

    def start_requests(self):
        for date in rrule(
            MONTHLY, dtstart=self.start_date.replace(day=1), until=self.end_date
        ):
            yield scrapy.Request(f"{self.BASE_URL}?mes={date.month}&ano={date.year}")

    def parse(self, response):
        diarios = response.xpath('//div[contains(@id, "diario")]')
        for diario in diarios:
            raw_date = diario.xpath(".//h3/text()").re_first(r"\d{2}/\d{2}/\d{4}")
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()

            date_within_expected_period = self.start_date <= date <= self.end_date
            if not date_within_expected_period:
                continue

            hrefs = diario.xpath(".//a/@href").getall()
            urls = [response.urljoin(link) for link in hrefs]
            item = Gazette(
                date=date,
                file_urls=urls,
                is_extra_edition=False,
                power="executive_legislative",
            )
            yield item
