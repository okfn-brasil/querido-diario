from datetime import date

import scrapy
from dateparser import parse
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RrBoaVistaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1400100"
    name = "rr_boa_vista"
    allowed_domains = ["boavista.rr.gov.br"]
    start_urls = ["https://www.boavista.rr.gov.br/diario-oficial"]
    start_date = date(2011, 1, 1)

    def parse(self, response):
        _check = response.css("#_Check::attr(value)").get()

        initial_date = date(self.start_date.year, self.start_date.month, 1)
        end_date = date.today()

        periods_of_interest = [
            (date.year, date.month)
            for date in rrule(freq=MONTHLY, dtstart=initial_date, until=end_date)
        ]
        for year, month in periods_of_interest:
            params = {
                "_Check": _check,
                "Numero": "",
                "Periodo": "{}{}".format(year, str(month).zfill(2)),
            }
            yield scrapy.FormRequest(
                url=response.url,
                formdata=params,
                callback=self.parse_period,
            )

    def parse_period(self, response):
        gazettes = response.css(".bldownload")
        for gazette in gazettes:
            gazette_date = gazette.css(".nome::text").re_first(r"\d{2} \w{3} \d{4}")
            gazette_date = parse(gazette_date, languages=["pt"]).date()

            edition_number = gazette.css(".nome::text").re_first(r"n. (\d+)")
            gazette_url = response.urljoin(gazette.css("a::attr(href)").get())

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                is_extra_edition=False,
                power="executive",
            )
