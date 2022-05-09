import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToAraguainaSpider(BaseGazetteSpider):
    name = "to_araguaina"
    TERRITORY_ID = "1702109"
    allowed_domains = [
        "diariooficial.araguaina.to.gov.br",
        "diariooficial.araguaina.tk",
    ]
    start_date = dt.date(2011, 12, 6)

    def start_requests(self):
        formatted_start_date = self.start_date.strftime("%d/%m/%Y")
        formatted_end_date = self.end_date.strftime("%d/%m/%Y")
        yield scrapy.Request(
            f"https://diariooficial.araguaina.to.gov.br/Pesquisa/?De={formatted_start_date}&Ate={formatted_end_date}"
        )

    def parse(self, response):
        editions = response.css("#ctl00_ContentPlaceHolder1_gvResultado tbody tr")
        for edition in editions:
            raw_date = edition.xpath(".//td[2]/text()").get()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
            edition_number = edition.xpath(".//td[1]/text()").re_first(r"\d+")

            gazette_item = Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive_legislative",
            )

            download_url = response.urljoin(edition.xpath(".//td[6]/a/@href").get())
            yield scrapy.Request(
                download_url,
                method="HEAD",
                callback=self.parse_gazette_download_url,
                cb_kwargs={"gazette_item": gazette_item},
            )

    def parse_gazette_download_url(self, response, gazette_item):
        gazette_item["file_urls"] = [response.url]
        yield gazette_item
