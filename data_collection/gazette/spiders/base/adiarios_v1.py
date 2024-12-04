import re
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAdiariosV1Spider(BaseGazetteSpider):
    """
    This base class deals with 'Layout 1' gazette pages, usually requested
    from https://{city_website}/diariooficial.php
    """

    def start_requests(self):
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")

        yield scrapy.Request(
            f"{self.BASE_URL}/diariooficial.php?dtini={start_date}&dtfim={end_date}",
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
        for element in response.css("#diario_lista"):
            date = element.css(".calendarioIcon::text").get().strip()
            date = datetime.strptime(date, "%d/%m/%Y").date()

            text = element.css("span strong::text").get()

            try:
                edition_number = re.search(r":\s*(\d+).*/", text).group(1)
            except AttributeError:
                edition_number = ""

            title = element.css("span::text").getall()[1]
            is_extra_edition = bool(
                re.search(
                    r"complementar|suplementar|extra|especial", title, re.IGNORECASE
                )
                or re.search(
                    r"complementar|suplementar|extra|especial", text, re.IGNORECASE
                )
            )
            power = self.get_power(title)

            gazette_id = re.search(
                r"id=(\d+)", element.css("a::attr(href)").get()
            ).group(1)

            file_url = f"{self.BASE_URL}/arquivos_download.php?id={gazette_id}&pg=diariooficial"

            yield Gazette(
                date=date,
                file_urls=[file_url],
                is_extra_edition=is_extra_edition,
                edition_number=edition_number,
                power=power,
            )

    def get_last_page_number(self, response):
        page_pagination = response.css(".pagination li a span::text").getall()
        page_numbers = [int(i) for i in page_pagination]
        last_page_index = max(page_numbers)
        return last_page_index

    def get_power(self, title):
        normalized_title = title.lower().strip()

        if "executivo" in normalized_title:
            power = "executive"
        elif "legislativo" in normalized_title:
            power = "legislative"
        else:
            # Categories like "Terceiro" and "Especial" occurs.
            # It's unclear whether it belongs to "executive" or "legislative" or both.
            # So, they'rs being considered "executive_legislative"
            power = "executive_legislative"

        return power
