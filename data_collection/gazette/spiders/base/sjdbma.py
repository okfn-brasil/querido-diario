import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SjdbmaGazetteSpider(BaseGazetteSpider):
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
        gazette_boxes = response.css(
            "div#edicoes-anteriores.table-responsive table.table.table-bordered tbody tr"
        )

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
                power="executive_legislative",
            )

        last_page = self.get_last_page(response)
        if page < last_page:
            yield scrapy.Request(
                url=self.get_url(page + 1), cb_kwargs={"page": page + 1}
            )

    def get_url(self, page=1):
        return f"{self.BASE_URL}?page={page}"

    @staticmethod
    def get_last_page(response):
        """
        Gets the last page number available in the pages navigation menu
        """
        pages = response.css("ul.pagination li.page-item a::text").getall()
        if len(pages) == 0:
            return 1
        return max([int(page) for page in pages if page.isnumeric()])

    def get_pdf_url(self, response_item):
        """
        Gets the url for the gazette inside one of the 'div#edicoes-anteriores' table
        """
        download_link = (
            response_item.css("td:nth-child(1) a::attr(href)").get().split("#")
        )
        url_base = self.allowed_domains[0]
        download_base = download_link[0]
        return f"https://{url_base}{download_base}"

    def get_gazette_date(self, response_item):
        """
        Get the date for the gazette inside one of the 'div#edicoes-anteriores' table
        """
        date = response_item.css("td:nth-child(3)::text").get().strip()
        date_cut = self.__format_date(date)
        return dateparser.parse(
            date_cut, date_formats=["%d - %B - %Y"], languages=["pt"]
        ).date()

    @staticmethod
    def __format_date(date):
        split_date = date.split(",")
        return split_date[1]

    def get_edition_number(self, response_item):
        """
        Get the edition number inside one of the 'div#edicoes-anteriores' table
        """
        text_edition = response_item.css("td:nth-child(1) a::text").get().strip()
        return self.__cut_edition_number(text_edition)

    @staticmethod
    def __cut_edition_number(text):
        split_text = text.split(" ")
        split_number_year = split_text[3].split("/")
        return split_number_year[0]
