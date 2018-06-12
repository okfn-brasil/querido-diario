
from dateparser import parse
from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ScBlumenauSpider(BaseGazetteSpider):
    TERRITORY_ID = '4202404'
    NEXT_PAGE_URL = 'https://www.diariomunicipal.sc.gov.br{}'
    POSSIBLE_GAZETTE_CSS = '.quiet'
    NEXT_PAGE_CSS = '.pagination li.next:not(.disabled) a::attr(href)'

    allowed_domains = ['diariomunicipal.sc.gov.br']
    name = 'sc_blumenau'
    start_urls = ['https://www.diariomunicipal.sc.gov.br/site/?r=site/index&q=cod_municipio%3A164']

    def parse(self, response):
        """
        @url https://www.diariomunicipal.sc.gov.br/site/?r=site/index&q=cod_municipio%3A164
        @returns requests 1
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """

        possible_gazettes = response.css(self.POSSIBLE_GAZETTE_CSS);
        for element in possible_gazettes:
            url = self.extract_url(element)
            if url:
                date = self.extract_date(element)

                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=False,
                    territory_id=self.TERRITORY_ID,
                    power='executive_legislature',
                    scraped_at=datetime.utcnow(),
                )
        
        next_page_url = self.extract_next_page_url(response)
        if next_page_url:
            yield Request(next_page_url)

    def extract_url(self, element):
        return element.css('a::attr(href)').extract_first()

    def extract_date(self, element):
        text = element.css('::text').extract_first()
        date = text[:10]
        return parse(date, languages=['pt']).date()

    def extract_next_page_url(self, response):
        next_page_path = response.css(self.NEXT_PAGE_CSS).extract_first()
        if next_page_path:
            return self.NEXT_PAGE_URL.format(next_page_path)
