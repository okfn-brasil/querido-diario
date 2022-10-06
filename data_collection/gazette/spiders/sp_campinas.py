from datetime import date

import scrapy
from dateparser import parse
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpCampinasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3509502"
    name = "sp_campinas"
    allowed_domains = ["campinas.sp.gov.br"]
    sp_campinas_url = "https://portal-api.campinas.sp.gov.br"
    url_base = "https://portal-api.campinas.sp.gov.br/api/v1/publicacoes-dom/all/{}{}?_format=json"
    start_date = date(1995, 10, 3)

    def start_requests(self):
        initial_date = date(self.start_date.year, self.start_date.month, 1)
        for monthly_date in rrule(
            freq=MONTHLY, dtstart=initial_date, until=self.end_date
        ):
            url = self.url_base.format(monthly_date.year, monthly_date.month)
            yield scrapy.Request(url)

    def parse(self, response):
        items = []
        data = response.json()
        for item in data:
            date = parse(item["dom_data_pub"], languages=["pt"]).date()
            url = f"{self.sp_campinas_url}{item['dom_arquivo']}"
            is_extra_edition = False
            power = "executive_legislative"
            items.append(
                Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=is_extra_edition,
                    power=power,
                )
            )
        return items
