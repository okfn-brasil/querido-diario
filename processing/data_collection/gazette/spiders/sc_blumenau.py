from datetime import datetime

from dateparser import parse
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ScBlumenauSpider(BaseGazetteSpider):
    TERRITORY_ID = "4202404"
    POSSIBLE_GAZETTE_CSS = ".quiet"
    NEXT_PAGE_CSS = ".pagination li.next:not(.disabled) a::attr(href)"

    allowed_domains = ["diariomunicipal.sc.gov.br"]
    name = "sc_blumenau"
    start_urls = [
        "https://www.diariomunicipal.sc.gov.br/site/?r=site/index&q=cod_municipio%3A164"
    ]

    def parse(self, response):
        """
        @url https://www.diariomunicipal.sc.gov.br/site/?r=site/index&q=cod_municipio%3A164
        @returns requests 1
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """

        possible_gazettes = response.css(self.POSSIBLE_GAZETTE_CSS)
        for element in possible_gazettes:
            url = element.css("a::attr(href)").extract_first()
            if url:
                date = parse(
                    element.css("::text").re_first("([\d]{2}\/[\d]{2}\/[\d]{4})"),
                    languages=["pt"],
                ).date()

                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=False,
                    territory_id=self.TERRITORY_ID,
                    power="executive_legislature",
                    scraped_at=datetime.utcnow(),
                )

        next_page_path = response.css(self.NEXT_PAGE_CSS).extract_first()
        if next_page_path:
            yield Request(response.urljoin(next_page_path))
