import datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MtRondonopolisSpider(BaseGazetteSpider):
    TERRITORY_ID = "5107602"
    name = "mt_rondonopolis"
    allowed_domains = ["rondonopolis.mt.gov.br"]
    BASE_URL = "http://www.rondonopolis.mt.gov.br/diario-oficial/"
    start_date = datetime.date(2004, 9, 1)

    custom_settings = {
        "DOWNLOAD_FAIL_ON_DATALOSS": False,
    }

    def start_requests(self):
        for date in rrule(DAILY, dtstart=self.start_date, until=self.end_date):
            search_date = date.strftime("%Y-%m-%d")
            yield scrapy.Request(
                f"{self.BASE_URL}?publish_date={search_date}&number=&q=",
                cb_kwargs={"gazette_date": date.date()},
            )

    def parse(self, response, gazette_date):
        for gazette in response.css("tbody tr"):
            edition_number = gazette.css("td:first-child::text").get()
            gazette_url = response.urljoin(gazette.css("td a::attr(href)").get())

            yield Gazette(
                date=gazette_date,
                file_urls=[gazette_url],
                is_extra_edition=False,
                edition_number=edition_number,
                power="executive",
            )
