import datetime

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpCampinasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3509502"
    name = "sp_campinas"
    allowed_domains = ["campinas.sp.gov.br"]
    sp_campinas_url = "https://portal-api.campinas.sp.gov.br"
    url_base = "https://portal-api.campinas.sp.gov.br/api/v1/publicacoes-dom/all/{}{}?_format=json"
    start_date = datetime.date(1995, 10, 3)

    def start_requests(self):
        initial_date = datetime.date(self.start_date.year, self.start_date.month, 1)
        for monthly_date in rrule(
            freq=MONTHLY, dtstart=initial_date, until=self.end_date
        ):
            url = self.url_base.format(monthly_date.year, monthly_date.month)
            yield scrapy.Request(url)

    def parse(self, response):
        for item in response.json():
            gazette_date = datetime.datetime.strptime(
                item["dom_data_pub"], "%d/%m/%Y"
            ).date()
            edition_number = item["dom_edicao"]

            is_extra_edition = False
            if item["dom_arquivo"] != "":
                gazette_url = response.urljoin(item["dom_arquivo"])
            elif item["dom_extra_arquivo"] != "":
                gazette_url = response.urljoin(item["dom_extra_arquivo"])
                is_extra_edition = True

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[
                    gazette_url,
                ],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )
