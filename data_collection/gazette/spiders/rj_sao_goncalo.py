from datetime import date, timedelta

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjSaoGoncaloSpider(BaseGazetteSpider):
    TERRITORY_ID = "3304904"
    DOWNLOAD_GAZETTE_URL = "https://servicos.pmsg.rj.gov.br/diario/{}.pdf"
    start_date = date(1998, 2, 3)
    end_date = date.today()
    name = "rj_sao_goncalo"
    allowed_domains = ["pmsg.rj.gov.br"]
    start_urls = ["https://www.pmsg.rj.gov.br/diario-oficial"]

    def parse(self, response):
        empty_files = [date(1998, 10, 15), date(2006, 2, 3), date(2006, 4, 27)]
        curr_date = self.end_date
        while curr_date >= self.start_date:
            url = self.DOWNLOAD_GAZETTE_URL.format(curr_date.strftime("%Y_%m_%d"))
            yield scrapy.Request(
                url,
                cb_kwargs={
                    "gazette_date": curr_date,
                    "file_urls": [url],
                },
                callback=self.parse_gazette,
                errback=self.errback_gazette,
            )
            while True:
                curr_date = curr_date - timedelta(days=1)
                # Known empty files are ignored so as not to break validation
                if curr_date not in empty_files:
                    break

    def parse_gazette(self, response, gazette_date, file_urls):
        yield Gazette(
            date=gazette_date,
            file_urls=file_urls,
            power="executive",
        )

    def errback_gazette(self, failure):
        # Gazette doesn't exist for some dates so response http 404 is not an error
        if not failure.check(HttpError):
            self.logger.error(repr(failure))
