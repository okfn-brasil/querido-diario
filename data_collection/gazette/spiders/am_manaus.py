import re
from datetime import date
from urllib.parse import unquote

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AmManausSpider(BaseGazetteSpider):
    TERRITORY_ID = "1302603"
    name = "am_manaus"
    allowed_domains = ["manaus.am.gov.br"]
    start_date = date(2000, 4, 19)

    NEXT_PAGE_CSS = "span.next a::attr(href)"
    DATE_CSS = "td:first-child span::text"
    GAZETTE_ROW_CSS = "table.listing tbody tr"
    PDF_HREF_CSS = "td:nth-child(2) a::attr(href)"
    PDF_TEXT_CSS = "td:nth-child(2) a:last-child::text"

    def start_requests(self):
        yield Request(
            url="http://dom.manaus.am.gov.br/diario-oficial-de-manaus",
            callback=self.parse_gazettes_list,
        )

    def parse_gazettes_list(self, response):
        for gazette in response.css(self.GAZETTE_ROW_CSS):
            url = gazette.css(self.PDF_HREF_CSS).get()
            date = gazette.css(self.DATE_CSS).get()
            date = dateparser.parse(date, languages=["pt"]).date()
            title = gazette.css(self.PDF_TEXT_CSS).get()
            is_extra_edition = "extra" in title.lower()
            filename = unquote(url).split("/")[-1]
            edition = re.search(
                r"(?:dom\d{4}|dom ?|^)(\d{3,4})", filename.lower()
            ).group(1)

            yield Gazette(
                date=date,
                edition_number=int(edition),
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive",
            )

        if self.start_date < date:
            yield from self.paginate(response)

    def paginate(self, response):
        next_page_href = response.css(self.NEXT_PAGE_CSS).get()
        if next_page_href:
            yield response.follow(url=next_page_href, callback=self.parse_gazettes_list)


class AmManausLegislativeSpider(BaseGazetteSpider):
    TERRITORY_ID = "1302603"
    name = "am_manaus_legislative"
    allowed_domains = ["cmm.am.gov.br"]
    start_date = date(2013, 7, 26)

    DATE_CSS = "td:first-child"
    GAZETTE_ROW_CSS = ".table-cmm tr"
    NEXT_PAGE_CSS = ".paging a.next::attr(href)"
    PDF_HREF_CSS = "td:last-child a::attr(href)"
    DATE_REGEX = r"[0-9]{2}/[0-9]{2}/[0-9]{4}"

    def start_requests(self):
        yield Request(
            "http://www.cmm.am.gov.br/diario-oficial", self.parse_gazettes_list
        )

    def parse_gazettes_list(self, response):
        for gazette in response.css(self.GAZETTE_ROW_CSS):
            if not gazette.css("td"):
                continue

            url = gazette.css(self.PDF_HREF_CSS).extract_first()
            date = gazette.css(self.DATE_CSS)
            date = date.re(self.DATE_REGEX).pop()
            date = dateparser.parse(date, languages=["pt"]).date()

            yield Gazette(
                date=date,
                file_urls=[url],
                power="legislative",
            )

        for url in response.css(self.NEXT_PAGE_CSS).extract():
            yield Request(url, self.parse_gazettes_list)
