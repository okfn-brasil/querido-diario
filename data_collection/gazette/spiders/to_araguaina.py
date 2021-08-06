import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToAraguainaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1702109"
    name = "to_araguaina"
    allowed_domains = [
        "diariooficial.araguaina.to.gov.br",
        "diariooficial.araguaina.tk",
    ]

    start_date = datetime.date(2011, 12, 5)

    def start_requests(self):
        initial_date = self.start_date.strftime("%d/%m/%Y")
        yield scrapy.Request(
            f"https://diariooficial.araguaina.to.gov.br/Pesquisa/?De={initial_date}"
        )

    def parse(self, response):
        gazettes = response.css("#ContentPlaceHolder1_gvResultado tbody tr")
        for gazette in gazettes:
            gazette_raw_date = gazette.xpath(".//td[2]/text()").get()
            gazette_date = datetime.datetime.strptime(
                gazette_raw_date, "%d/%m/%Y"
            ).date()

            edition = gazette.xpath(".//td[1]/text()")
            edition_number = edition.re_first(r"\d+")
            is_extra_edition = "suplemento" in edition.get().lower()

            gazette_item = Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive",
            )

            download_url = response.urljoin(gazette.xpath(".//td[6]/a/@href").get())
            yield scrapy.Request(
                download_url,
                method="HEAD",
                callback=self.parse_gazette_download_url,
                cb_kwargs={"item": gazette_item},
            )

    def parse_gazette_download_url(self, response, item):
        item["file_urls"] = [response.url]
        yield item
