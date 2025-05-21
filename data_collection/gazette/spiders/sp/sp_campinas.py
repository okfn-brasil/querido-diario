import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class SpCampinasSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "3509502"
    name = "sp_campinas"
    allowed_domains = ["campinas.sp.gov.br"]
    sp_campinas_url = "https://portal-api.campinas.sp.gov.br"
    url_base = "https://portal-api.campinas.sp.gov.br/api/v1/publicacoes-dom/all/{}?_format=json"
    start_date = datetime.date(1995, 10, 3)

    def start_requests(self):
        for date in monthly_sequence(self.start_date, self.end_date, format="%Y%m"):
            yield scrapy.Request(self.url_base.format(date))

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
