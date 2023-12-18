from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


# Create a class for the spider
class MgPiumhiSpider(BaseGazetteSpider):
    name = "mg_piumhi"
    TERRITORY_ID = "3151503"
    allowed_domains = ["prefeiturapiumhi.mg.gov.br"]
    start_date = date(2023, 9, 11)
    start_urls = ["https://diario-oficial.prefeiturapiumhi.mg.gov.br/"]


    def parse(self, response):
        gazettes = response.css(
            "div.jet-listing-grid__items div.jet-listing-grid__item"
        )
        for gazette in gazettes:
            gazette_date = gazette.css(
                "div.jet-listing-dynamic-field__content::text"
            ).re_first(r"(\d{2}/\d{2}/\d{4})")

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            file_urls = gazette.css("a::attr(href)").getall()
            edition_number = gazette.css("h2::text").re_first(r"\d+")
            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=file_urls,
                power="executive",
                is_extra_edition=False,
            )
