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
    end_date = datetime.date.today()

    def start_requests(self):
        for date in rrule(DAILY, dtstart=self.start_date, until=self.end_date):
            yield scrapy.Request(
                f"{self.BASE_URL}?publish_date={date.date()}&number=&q=",
                cb_kwargs={"gazette_date": date.date()},
            )

    def parse(self, response, gazette_date):
        if response.css("tbody tr").get() is not None:
            for gazette in response.css("tbody tr"):
                edition = gazette.css("td:first-child::text").get()
                pdf_url = response.urljoin(gazette.css("td a::attr(href)").get())

                if pdf_url.endswith(".pdf") or pdf_url.endswith(".zip"):
                    item = Gazette(
                        date=gazette_date,
                        file_urls=[pdf_url],
                        is_extra_edition=False,
                        edition_number=edition,
                        power="executive",
                    )

                    yield scrapy.Request(
                        pdf_url,
                        callback=self.http_response,
                        errback=self.http_error,
                        cb_kwargs={"item": item},
                    )

                else:
                    pass

    def http_response(self, response, item):
        yield Gazette(
            **item,
        )

    def http_error(self, failure):
        pass
