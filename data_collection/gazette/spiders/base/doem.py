from datetime import date

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DoemGazetteSpider(BaseGazetteSpider):
    """
    Base spider for all cities listed on https://doem.org.br
    """

    allowed_domains = ["doem.org.br"]
    start_date = date(2009, 1, 1)

    def start_requests(self):
        yield scrapy.Request(self.get_url(), callback=self.parse_pagination)

    def parse_pagination(self, response):
        """
        This parse function is used to get all the pages available and
        return request object for each one
        """
        return [
            scrapy.Request(self.get_url(page), callback=self.parse)
            for page in range(1, 1 + self.get_last_page(response))
        ]

    def parse(self, response):
        """
        Parse each page from the results page and yield the gazette issues available.
        """
        gazette_boxes = response.css("div.box-diario")

        for gazette_box in gazette_boxes:
            file_url = self.get_pdf_url(gazette_box)
            date = self.get_gazette_date(gazette_box)
            edition_number = self.get_edition_number(gazette_box)
            yield Gazette(
                date=date,
                file_urls=[file_url],
                edition_number=edition_number,
                power="executive_legislative",
            )

    def get_url(self, page=None):
        url = f"https://doem.org.br/{self.state_city_url_part}"
        start_date = self.start_date.strftime("%Y-%m-%d")
        page_param = f"&page={page}" if page is not None else ""
        return f"{url}/pesquisar?data_inicial={start_date}{page_param}"

    def get_last_page(self, response):
        """
        Gets the last page number available in the pages navigation menu
        """
        pages = response.css("ul.pagination li a::text").getall()
        if len(pages) == 0:
            return 1
        return max([int(page) for page in pages if page.isnumeric()])

    def get_pdf_url(self, response_item):
        """
        Gets the url for the gazette inside one of the 'box-diario' divs
        """
        preview_link = response_item.css(
            "a[title='Baixar Publicação']::attr(href)"
        ).get()
        return preview_link.replace("previsualizar", "baixar")

    def get_gazette_date(self, response_item):
        """
        Get the date for the gazette inside one of the 'box-diario' divs
        """
        date = response_item.css("span.data-diario::text").get().strip()
        return dateparser.parse(date, languages=["pt"]).date()

    def get_edition_number(self, response_item):
        """
        Get the edition number inside one of the 'box-diario' divs
        """
        edition_text = response_item.css("h2::text").get()
        edition_number = edition_text.strip().split(" ")[1]
        return int(edition_number) if edition_number.isnumeric() else None
