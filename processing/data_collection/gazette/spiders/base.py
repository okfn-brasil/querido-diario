# -*- coding: utf-8 -*-
import re
from datetime import datetime

import dateparser
import scrapy

from gazette.items import Gazette


class BaseGazetteSpider(scrapy.Spider):
    def __init__(self, start_date=None, *args, **kwargs):
        super(BaseGazetteSpider, self).__init__(*args, **kwargs)

        if start_date is not None:
            parsed_data = dateparser.parse(start_date)
            if parsed_data is not None:
                self.start_date = parsed_data.date()


class FecamGazetteSpider(scrapy.Spider):

    URL = "https://www.diariomunicipal.sc.gov.br/site/"
    total_pages = None

    def start_requests(self):
        if self.total_pages is None:
            yield scrapy.Request(
                f"{self.URL}?q={self.FECAM_QUERY}", callback=self.parse
            )

    def parse(self, response):
        if self.total_pages is None:
            self.total_pages = self.get_last_page(response)
        # Get gazzete info
        documents = self.get_documents_links_date(response)
        for d in documents:
            yield self.get_gazzete(d)
        if self.total_pages > 1:
            yield scrapy.Request(
                f"{self.URL}?q={self.FECAM_QUERY}&Search_page={self.total_pages}",
                callback=self.parse,
            )
            self.total_pages = self.total_pages - 1

    def get_documents_links_date(self, response):
        """
        Method to get all the relevant documents list and their dates from the page
        """
        documents = []
        elements = response.xpath('/html/body/div[1]/div[3]/div[5]/p[@class="quiet"]')
        for e in elements:
            if "Visualizar" in e.xpath("a[1]/text()").get():
                # The element does not contain the element with the file URL.
                # Thus, the URL is in the preceding title
                link = e.xpath("preceding-sibling::h4[1]/a/@href").get().strip()
            else:
                link = e.xpath("a[1]/@href").get().strip()
            date = e.re_first("\d{2}/\d{2}/\d{4}").strip()
            documents.append((link, date))
        return documents

    @staticmethod
    def get_last_page(response):
        """
        Get the last page number available in the pages navigation menu
        """
        href = response.xpath(
            "/html/body/div[1]/div[3]/div[4]/div/div/ul/li[14]/a/@href"
        ).get()
        result = re.search("Search_page=(\d+)", href)
        if result is not None:
            return int(result.groups()[0])

    def get_gazzete(self, document):
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
            territory_id=self.TERRITORY_ID,
            scraped_at=datetime.utcnow(),
        )
