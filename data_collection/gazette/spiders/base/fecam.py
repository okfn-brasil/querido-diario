import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class FecamGazetteSpider(BaseGazetteSpider):

    URL = "https://www.diariomunicipal.sc.gov.br/site/"
    total_pages = None

    def start_requests(self):
        yield scrapy.Request(
            f"{self.URL}?q={self.FECAM_QUERY}", callback=self.parse_pagination
        )

    def parse_pagination(self, response):
        """
        This parse function is used to get all the pages available and
        return request object for each one
        """
        return [
            scrapy.Request(
                f"{self.URL}?q={self.FECAM_QUERY}&Search_page={i}", callback=self.parse
            )
            for i in range(1, self.get_last_page(response) + 1)
        ]

    def parse(self, response):
        """
        Parse each page from the gazette page.
        """
        # Get gazzete info
        documents = self.get_documents_links_date(response)
        for d in documents:
            yield self.get_gazette(d)

    def get_documents_links_date(self, response):
        """
        Method to get all the relevant documents list and their dates from the page
        """
        documents = []
        titles = response.css("div.row.no-print h4")
        for title in titles:
            title_sibling_link = title.xpath("following-sibling::a[2]")
            if "[Abrir/Salvar Original]" in title_sibling_link.xpath("./text()").get():
                link = title_sibling_link.xpath("./@href").get().strip()
            else:
                link = title.xpath("./a/@href").get().strip()
            date = (
                title.xpath("following-sibling::span[1]")
                .re_first(r"\d{2}/\d{2}/\d{4}")
                .strip()
            )
            documents.append((link, date))
        return documents

    @staticmethod
    def get_last_page(response):
        """
        Get the last page number available in the pages navigation menu
        """
        href = response.xpath(
            "/html/body/div[1]/div[4]/div[4]/div/div/ul/li[14]/a/@href"
        ).get()
        result = re.search(r"Search_page=(\d+)", href)
        if result is not None:
            return int(result.groups()[0])

    def get_gazette(self, document):
        """
        Transform the tuple returned by get_documents_links_date and returns a
        Gazette item
        """
        if document[1] is None or len(document[1]) == 0:
            raise "Missing document date"
        if document[0] is None or len(document[0]) == 0:
            raise "Missing document URL"

        return Gazette(
            date=dateparser.parse(document[1], languages=("pt",)).date(),
            file_urls=(document[0],),
            power="executive",
        )
