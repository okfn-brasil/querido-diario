import datetime as dt

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjNovaIguacu(BaseGazetteSpider):
    TERRITORY_ID = "3303500"
    name = "rj_nova_iguacu"
    allowed_domains = ["novaiguacu.rj.gov.br"]
    start_date = dt.date(2014, 1, 6)
    BASE_URL = "https://www.novaiguacu.rj.gov.br/diario-oficial/"

    def start_requests(self):
        for date in rrule(DAILY, dtstart=self.start_date, until=self.end_date):
            yield scrapy.Request(
                f"{self.BASE_URL}?data={date.isoformat()}",
                cb_kwargs={"date": date.date()},
            )

    def parse(self, response, date):
        editions = response.css("div.caption a")
        if not editions:
            return

        for edition in editions:
            url = edition.attrib["href"]
            if not url:
                continue

            title = edition.xpath("./text()").get()
            is_extra_edition = (
                "extra" in title.lower() if title else "extra" in url.lower()
            )
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive",
            )
