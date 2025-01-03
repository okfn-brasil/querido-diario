import re
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAdiariosV2Spider(BaseGazetteSpider):
    """
    This base class deals with 'Layout 2' gazette pages, usually requested
    from https://{city_website}/jornal.php
    """

    def start_requests(self):
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")

        yield scrapy.Request(
            f"{self.BASE_URL}/jornal.php?dtini={start_date}&dtfim={end_date}",
            callback=self.parse_pagination,
        )

    def parse_pagination(self, response):
        last_page_number = self.get_last_page_number(response)

        for page_number in range(1, last_page_number):
            yield scrapy.Request(
                f"{response.url}&pagina={page_number}", callback=self.parse_page
            )

        yield from self.parse_page(response)

    def parse_page(self, response):
        # [1:] => first element is table header
        elements = response.css("table tr")[1:]

        for element in elements:
            raw_date = element.css("td[data-title='Publicação']::text").get()
            gazette_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            edition_number, is_extra_edition = self.get_edition_info(element)

            gazette_id = re.search(
                r"id=(\d+)", element.css("td a").attrib["href"]
            ).group(1)

            gazette_item = {
                "date": gazette_date,
                "edition_number": edition_number,
                "is_extra_edition": is_extra_edition,
                "power": "executive",
            }

            yield scrapy.Request(
                url=f"{self.BASE_URL}/jornal.php?id={gazette_id}",
                callback=self.intermediary_page,
                cb_kwargs={"gazette_item": gazette_item},
            )

    def get_last_page_number(self, response):
        page_pagination = response.css(".pagination li a span::text").getall()
        last_page_index = max([int(i) for i in page_pagination])
        return last_page_index

    def intermediary_page(self, response, gazette_item):
        gazette_path = response.css("div.public_paginas > div.titulo > a").attrib[
            "href"
        ]
        gazette_url = f"{self.BASE_URL}/{gazette_path}"

        yield Gazette(
            **gazette_item,
            file_urls=[gazette_url],
        )

    def get_edition_info(self, element):
        edition_number = element.css("td[data-title='Número']::text").get()

        if edition_number is None:
            return "", False

        is_extra_edition = bool(
            re.search(
                r"complementar|suplement|extra|especial|anexo",
                edition_number.lower(),
                re.IGNORECASE,
            )
        )
        return edition_number.strip(), is_extra_edition
