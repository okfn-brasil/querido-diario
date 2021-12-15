import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class FecamGazetteSpider(BaseGazetteSpider):

    URL = "https://www.diariomunicipal.sc.gov.br/site/"
    total_pages = None
    category = None

    def __init__(self, start_date=None, *args, **kwargs):
        super().__init__(start_date, *args, **kwargs)
        self.category = kwargs.get("gazette_category", None)

    def _build_query_string(self, search_page=None):
        if self.FECAM_QUERY is None:
            raise Exception("Missing FECAM_QUERY")
        query = f"q={self.FECAM_QUERY}"
        if self.category is not None:
            query = f"{query}+categoria:{self.category}"
        if self.start_date is not None:
            date_string = self.start_date.strftime("%Y-%m-%dT00:00:00Z")
            query = f"{query}+data:[{date_string}+TO+*]"
        if search_page is not None:
            query = f"{query}&AtoASolrDocument_page={search_page}"
        self.logger.debug(query)
        return query

    def start_requests(self):
        query_string = self._build_query_string()
        yield scrapy.Request(
            f"{self.URL}?{query_string}", callback=self.parse_pagination
        )

    def parse_pagination(self, response):
        """
        This parse function is used to get all the pages available and
        return request object for each one
        """

        requests = []
        for i in range(1, self.get_last_page(response) + 1):
            query_string = self._build_query_string(i)
            requests.append(
                scrapy.Request(f"{self.URL}?{query_string}", callback=self.parse)
            )
        return requests

    def parse(self, response):
        """
        Parse each page from the gazette page.
        """
        documents = self.get_documents_links_date(response)
        for d in documents:
            yield self.get_gazette(d)
        # Gazettes of the "AutoPublicação" type needs special handling
        return self.get_autopublicacoes_gazettes(response)

    def get_autopublicacao_link(self, response, metadata, gazette_title):
        """
        Builds a request object to download the "AutoPublicação" gazette.
        """
        date = metadata.re_first(r"\d{2}/\d{2}/\d{4}").strip()
        category = metadata.xpath("./text()").getall()[1].split("-")[1].strip().lower()
        return response.follow(
            self.get_file_link_from_title(gazette_title),
            callback=self.parse_autopublicacao,
            cb_kwargs={"date": date, "category": category},
        )

    def parse_autopublicacao(self, response, date, category):
        """
        Parser function called when a "AutoPublicação" gazette is downloaded.

        Returns the Gazette object.
        """
        return self.get_gazette(
            {"link": response.url, "date": date, "category": category}
        )

    def get_autopublicacoes_gazettes(self, response):
        """
        Get all the links for "AutoPublicação" gazettes.

        This returns a request objects which will download the file.
        """
        titles = response.css("div.row.no-print h4")
        for title in titles:
            metadata = title.xpath("following-sibling::span[1]")
            if self.is_autopublicacao(metadata):
                yield self.get_autopublicacao_link(response, metadata, title)

    def get_file_link_from_title(self, title):
        """
        Get the file link from the gazette's title.
        """
        title_sibling_link = title.xpath("following-sibling::a[2]")
        if "[Abrir/Salvar Original]" in title_sibling_link.xpath("./text()").get():
            return title_sibling_link.xpath("./@href").get().strip()
        return title.xpath("./a/@href").get().strip()

    def is_autopublicacao(self, metadata):
        """
        Checks if the item from the given metadadata is an "autopublicação".
        """
        autopublicacao = metadata.xpath("./span/text()").get().strip().lower()
        return autopublicacao is not None and autopublicacao == "autopublicação"

    def get_documents_links_date(self, response):
        """
        Method to get all the relevant documents list and their dates from the page
        """
        documents = []
        titles = response.css("div.row.no-print h4")
        for title in titles:
            metadata = title.xpath("following-sibling::span[1]")

            if self.is_autopublicacao(metadata):
                # we skip "auto publicações" because they require an redirect
                # in order to get the file. Thus, they are handle in another place.
                continue

            link = self.get_file_link_from_title(title)
            date = metadata.re_first(r"\d{2}/\d{2}/\d{4}").strip()
            category = metadata.xpath("./text()").get().split("-")[1].strip().lower()
            documents.append({"link": link, "date": date, "category": category})
        return documents

    @staticmethod
    def get_last_page(response):
        """
        Get the last page number available in the pages navigation menu
        """
        href = response.css(
            "div.pagination.pagination-centered ul#yw4 li.last a::attr(href)"
        ).get()
        result = re.search(r"AtoASolrDocument_page=(\d+)", href)
        if result is not None:
            return int(result.groups()[0])

    def get_gazette(self, document):
        """
        Transform the tuple returned by get_documents_links_date and returns a
        Gazette item
        """
        self.logger.debug(f"Creating gazette: {document}")
        if "date" not in document:
            raise "Missing document date"
        if "link" not in document:
            raise "Missing document URL"

        return Gazette(
            date=dateparser.parse(document["date"], languages=("pt",)).date(),
            file_urls=(document["link"],),
            power="executive",
            category=document.get("category", "unknown"),
        )
