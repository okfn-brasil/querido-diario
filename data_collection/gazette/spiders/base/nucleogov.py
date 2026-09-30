import json
from datetime import datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class NucleoGovGazetteSpider(BaseGazetteSpider):
    def start_requests(self):
        days = rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date)
        for day in days:
            yield scrapy.Request(self.url_base.format(day.strftime("%Y-%m-%d")))

    def parse(self, response):
        data = json.loads(response.text)

        gazettes = data.get("data")
        for gazette in gazettes:
            gazette_urls = []

            if gazette.get("media_legacy"):
                gazette_urls.append(gazette.get("media_legacy"))
            else:
                midias = gazette.get("midias")

                for midia in midias:
                    gazette_urls.append(midia.get("url"))

            gazette_date = datetime.strptime(gazette.get("data"), "%Y-%m-%d")
            edition_number = gazette.get("numero")

            yield Gazette(
                date=gazette_date.date(),
                file_urls=gazette_urls,
                edition_number=edition_number,
                power="executive",
                is_extra_edition=False,
            )
