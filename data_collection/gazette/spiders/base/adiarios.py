import datetime
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AdiariosGazetteSpider(BaseGazetteSpider):
    def start_requests(self):
        yield scrapy.Request(
            self.get_url(page_number=None), callback=self.parse_pagination
        )

    def parse_pagination(self, response):
        """
        Yeilds a request for each page available in the pagination
        """
        last_page_number = self.get_last_page_number(response)
        for i in range(last_page_number + 1):
            yield scrapy.Request(self.get_url(page_number=i), callback=self.parse_page)

    def parse_page(self, response):
        """
        Parse a page from the pagination and yield the gazettes
        """
        for element in response.css("#diario_lista"):
            text = "".join(element.css("span ::text").getall())
            edition_number = re.search(r"(\d+)", text).group(1)
            is_extra_edition = bool(
                re.search(r"complementar|suplementar|extra", text, re.IGNORECASE)
            )
            power = "legislative" if "legislativo" in text.lower() else "executive"

            date = element.css(".calendarioIcon::text").get().strip()
            date = datetime.datetime.strptime(date, "%d/%m/%Y").date()

            gazette_id = re.search(
                r"id=(\d+)", element.css("a::attr(href)").get()
            ).group(1)
            file_url = f"{self.BASE_URL}/arquivos_download.php?id={gazette_id}&pg=diariooficial"

            yield Gazette(
                date=date,
                file_urls=[
                    file_url,
                ],
                is_extra_edition=is_extra_edition,
                edition_number=edition_number,
                power=power,
            )

    def get_url(self, page_number):
        """
        Get the URL of a given page index in the range of self.start_date to self.end_date
        """
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")
        if page_number is None:
            url = (
                f"{self.BASE_URL}/diariooficial.php?dtini={start_date}&dtfim={end_date}"
            )
        else:
            url = f"{self.BASE_URL}/diariooficial.php?dtini={start_date}&dtfim={end_date}&pagina={page_number}"
        return url

    def get_last_page_number(self, response):
        """
        Get the last page index from the pagination
        """
        page_pagination = response.css(".pagination li a::attr(href)").getall()
        page_numbers = [
            int(re.search(r"pagina=(\d+)", i).group(1)) for i in page_pagination
        ]
        last_page_index = max(page_numbers)
        return last_page_index
