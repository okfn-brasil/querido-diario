import datetime

import scrapy
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

MONTHS_MAP = {
    month: value
    for value, month in enumerate(
        [
            "JAN",
            "FEV",
            "MAR",
            "ABR",
            "MAI",
            "JUN",
            "JUL",
            "AGO",
            "SET",
            "OUT",
            "NOV",
            "DEZ",
        ],
        1,
    )
}


class ScJoinvilleSpider(BaseGazetteSpider):
    TERRITORY_ID = "4209102"
    allowed_domains = ["joinville.sc.gov.br"]
    name = "sc_joinville"
    start_urls = ["https://www.joinville.sc.gov.br/jornal/index/page/1"]
    start_date = datetime.date(2009, 1, 2)

    def parse(self, response):
        follow_next_page = True
        extracted_dates = set()
        for gazette in response.css("ul.jornal li"):
            gazette_date = self._extract_date(gazette)
            extracted_dates.add(gazette_date)
            gazette_url = response.urljoin(
                gazette.xpath(
                    ".//a[not(contains(@href, 'visualizaranexos'))]/@href"
                ).get()
            )
            edition_number = gazette.xpath(".//text()").re_first(r"N.\s(\d+)")
            is_extra_edition = bool(gazette.css(".edicao_extraordinaria"))

            if self.start_date <= gazette_date <= self.end_date:
                item = Gazette(
                    date=gazette_date,
                    edition_number=edition_number,
                    file_urls=[
                        gazette_url,
                    ],
                    is_extra_edition=is_extra_edition,
                    power="executive_legislative",
                )
                view_supplement_url = gazette.xpath(
                    ".//a[contains(@href, 'visualizaranexos')]/@href"
                ).get()
                if not view_supplement_url:
                    yield item
                else:
                    yield scrapy.Request(
                        response.urljoin(view_supplement_url),
                        callback=self.process_supplement,
                        cb_kwargs={
                            "item": item,
                        },
                    )

        follow_next_page = min(extracted_dates) >= self.start_date
        if follow_next_page:
            next_page_url = response.css("li.next a::attr(href)").get()
            yield Request(next_page_url)

    def _extract_date(self, element):
        full_date = element.css("span.article-date::text").re(
            r"([\d]+)[ |]+([\w]+)[ |]+([\d]+)"
        )
        day, month, year = full_date
        return datetime.date(int(year), MONTHS_MAP[month], int(day))

    def process_supplement(self, response, item):
        item["file_urls"] = [
            response.urljoin(url) for url in response.css("a::attr(href)").getall()
        ]
        yield item
