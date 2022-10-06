import datetime as dt

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpCampinasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3509502"
    name = "sp_campinas"
    allowed_domains = ["campinas.sp.gov.br"]
    sp_campinas_url = "https://portal-api.campinas.sp.gov.br"
    selector_url = "https://portal-api.campinas.sp.gov.br/api/v1/publicacoes-dom/all/{}{}?_format=json"

    def start_requests(self):
        today = dt.date.today()
        next_year = today.year + 1
        for year in range(2015, next_year):
            for month in range(1, 13):
                if year == today.year and month > today.month:
                    return

                url = self.selector_url.format(year, month)
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
