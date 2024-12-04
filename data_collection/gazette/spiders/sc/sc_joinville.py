import datetime

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ScJoinvilleSpider(BaseGazetteSpider):
    TERRITORY_ID = "4209102"
    PDF_URL = "https://www.joinville.sc.gov.br{}"

    GAZETTE_ELEMENT_CSS = "ul.jornal li"
    NEXT_PAGE_CSS = "ul.pagination li.next a::attr(href)"
    DATE_CSS = "span.article-date::text"
    EXTRA_EDITION_CSS = "span.edicao_extraordinaria::text"
    DATE_REGEX = r"([\d]+)[ |]+([\w]+)[ |]+([\d]+)"

    allowed_domains = ["joinville.sc.gov.br"]
    name = "sc_joinville"
    start_urls = ["https://www.joinville.sc.gov.br/jornal/index/page/1"]
    start_date = datetime.date(2009, 1, 2)

    def parse(self, response):
        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            date = self.extract_date(element)
            url = self.extract_url(element)
            is_extra_edition = self.extract_extra_edition_info(element)
            edition_number = element.xpath(".//text()").re_first(r"N.\s(\d+)")

            if date >= self.start_date and date <= self.end_date:
                yield Gazette(
                    date=date,
                    file_urls=[url],
                    edition_number=edition_number,
                    is_extra_edition=is_extra_edition,
                    power="executive_legislative",
                )
            else:
                if date < self.start_date:
                    return

        for url in response.css(self.NEXT_PAGE_CSS).getall():
            yield Request(url)

    def extract_date(self, element):
        date = element.css(self.DATE_CSS).re(self.DATE_REGEX)
        date = "/".join(date)
        return dateparser.parse(date, languages=["pt"]).date()

    def extract_url(self, element):
        path = element.css("a::attr(href)").get()
        return self.PDF_URL.format(path)

    def extract_extra_edition_info(self, element):
        extra_edition_data = element.css(self.EXTRA_EDITION_CSS).get()
        return extra_edition_data == "Edição Extraordinária"
