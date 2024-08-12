import re
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpBatataisSpider(BaseGazetteSpider):
    name = "sp_batatais"
    TERRITORY_ID = "3505906"
    allowed_domains = ["www.batatais.sp.gov.br"]
    start_urls = ["https://www.batatais.sp.gov.br/diario-oficial"]
    start_date = datetime(2021, 10, 27).date()

    def start_requests(self):
        page = 1

        start_url = f"{self.start_urls[0]}?p={page}"

        yield scrapy.Request(start_url, cb_kwargs={"page": page})

    def _pagination_requests(self, response, page):
        if page == 1:
            pages = response.xpath(
                "/html/body/main/section[2]/div/div/div[2]/nav/ul/li/a/text()"
            )
            last_page = int(pages[-1].get())

            for next_page in range(2, last_page + 1):
                next_page_url = f"{self.start_urls[0]}?p={next_page}"

                yield scrapy.Request(next_page_url, cb_kwargs={"page": page})

    def parse(self, response, page):
        gazettes_xpath = "/html/body/main/section[2]/div/div/div[2]/div"

        gazettes = response.xpath(gazettes_xpath)

        extra_regex = re.compile(r"(?i)extra")
        edition_number_regex = re.compile(r"\d+(-[A-Za-z])?\/\d{4}")

        for gazette in gazettes:
            is_extra_edition = False
            edition = gazette.xpath("div/span/text()")
            edition_description = edition[0].get()
            if extra_regex.search(edition_description):
                is_extra_edition = True

            edition_number = edition_number_regex.search(edition_description).group()

            edition_date = datetime.strptime(
                edition[1].get().split()[-1], "%d/%m/%Y"
            ).date()
            edition_file = gazette.xpath("div[@class='card-buttons']/a/@href").get()

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[edition_file],
                power="executive",
            )
        yield from self._pagination_requests(response, page)
