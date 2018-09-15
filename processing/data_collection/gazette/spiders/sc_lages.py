
from dateparser import parse
from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ScLagesSpider(BaseGazetteSpider):
    TERRITORY_ID = "4209300"
    POSSIBLE_GAZETTE_CSS = ".quiet"
    NEXT_PAGE_CSS = ".pagination li.next:not(.disabled) a::attr(href)"

    allowed_domains = ["diariomunicipal.sc.gov.br"]
    name = "sc_lages"
    start_urls = [
        "https://www.diariomunicipal.sc.gov.br/site/?r=site/index&q=cod_municipio%3A277"
    ]

    def parse(self, response):
        """
        @url https://www.diariomunicipal.sc.gov.br/site/?r=site/index&q=cod_municipio%3A277
        @returns requests 1
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """

        possible_gazettes = response.css(self.POSSIBLE_GAZETTE_CSS)
        for element in possible_gazettes:
            url = element.css("a::attr(href)").extract_first()
            if url:
                date = self.extract_date(element)

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

    def extract_date(self, element):
        text = element.css("::text").extract_first()
        date = text[:10]
        return parse(date, languages=["pt"]).date()
