import datetime as dt

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DoemGazetteSpider(BaseGazetteSpider):
    """
    Base spider for all cities listed on https://doem.org.br
    """

    allowed_domains = ["doem.org.br"]
    start_date = dt.date(2009, 1, 1)

    def start_requests(self):
        yield scrapy.Request(self.get_url())

    def parse_pagination(self, response):
        """
        This parse function is used to get all the pages available and
        return request object for each one
        """
        return [
            scrapy.Request(self.get_url(page), callback=self.parse)
            for page in range(1, 1 + self.get_last_page(response))
        ]

    def parse(self, response, page=1):
        """
        Parse each page from the results page and yield the gazette issues available.
        """
        gazette_boxes = response.css("div.box-diario")

        for gazette_box in gazette_boxes:
            file_url = self.get_pdf_url(gazette_box)
            date = self.get_gazette_date(gazette_box)
            edition_number = self.get_edition_number(gazette_box)

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield Gazette(
                date=date,
                file_urls=[file_url],
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive_legislative",
            )

        last_page = self.get_last_page(response)
        if page < last_page:
            yield scrapy.Request(
                url=self.get_url(page + 1), cb_kwargs={"page": page + 1}
            )

    def get_url(self, page=1):
        url = f"https://doem.org.br/{self.state_city_url_part}"
        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")
        return f"{url}/pesquisar?data_inicial={start_date}&data_final={end_date}&page={page}"

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
        return response_item.css("h2::text").re_first(r"Edição\s+([.\d]+)")
