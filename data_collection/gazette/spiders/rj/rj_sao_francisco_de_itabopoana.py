import re
from datetime import date

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class RjSaoFranciscoDeItabopoanaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3304755"
    name = "rj_sao_francisco_de_itabopoana"
    allowed_domains = ["pmsfi.rj.gov.br"]
    start_urls = ["https://pmsfi.rj.gov.br/diariooficial/"]
    start_date = date(2016, 12, 1)

    def parse(self, response):
        year_links = response.css("div.pd-subcategory a::attr(href)").getall()

        for link in year_links:
            yield response.follow(link, self.parse_year_page)

    def parse_year_page(self, response):
        month_links = response.css("div.pd-subcategory a::attr(href)").getall()

        for link in month_links:
            yield scrapy.Request(
                url=response.urljoin(link), callback=self.parse_month_page
            )

    def parse_month_page(self, response):
        gazettes = response.css("div.pd-filebox, div.pd-document, .itemContainer")

        if not gazettes:
            return

        for gazette in gazettes:
            download_url = gazette.css('a[href*="download"]::attr(href)').get()
            if not download_url:
                continue

            date_string = None
            details_button = gazette.css(
                'a[onmouseover*="overlib"]::attr(onmouseover)'
            ).get()

            gazette_date = get_date_from_text(details_button)

            if gazette_date > self.end_date:
                continue

            if gazette_date < self.start_date:
                return

            if details_button:
                date_match = re.search(
                    r"Data:.*?<div class=\\'pd-fl-m\\'>(\d{1,2}\s+\w+\s+\d{4})<\/div>",
                    details_button,
                    re.IGNORECASE,
                )
                if date_match:
                    date_string = date_match.group(1)

            if not date_string:
                continue

            title = gazette.css("div.pd-title::text").get()

            is_extra = "suplemento" in title.lower() or "extra" in title.lower()
            edition_number_match = re.search(r"(\d+)", title)
            edition_number = edition_number_match.group(1)

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra,
                file_urls=[response.urljoin(download_url)],
                power="executive",
            )
