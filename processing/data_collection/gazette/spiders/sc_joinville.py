import re
import dateparser

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette

class GazetteElement:
    DATE_CSS = 'span.article-date::text'
    MUNICIPALITY_ID = '4209102'
    PDF_URL = 'https://www.joinville.sc.gov.br{}'

    def __init__(self, element):
        self.element = element

    def date(self):
        date_str = self.element.css(self.DATE_CSS)[-1].extract()
        return dateparser.parse(date_str, languages=['pt']).date()

    def url(self):
        path = self.element.css('a::attr(href)').extract_first()
        return self.PDF_URL.format(path)

    def to_gazette(self):
        return Gazette(
            date=self.date(),
            file_urls=[self.url()],
            is_extra_edition=False,
            municipality_id=self.MUNICIPALITY_ID,
            power='executive_legislature',
            scraped_at=datetime.utcnow(),
        )


class ScJoinvilleSpider(Spider):
    GAZETTE_ELEMENT_CSS = 'ul.jornal li'
    NEXT_PAGE_CSS = 'ul.pagination li.next a::attr(href)'

    allowed_domains = ['joinville.sc.gov.br']
    name = 'sc_joinville'
    start_urls = ['https://www.joinville.sc.gov.br/jornal/index/page/1']

    def parse(self, response):
        """
        @url http://www.joinville.sc.gov.br/jornal/index/page/1
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            yield GazetteElement(element).to_gazette()

        for url in response.css(self.NEXT_PAGE_CSS).extract():
            yield Request(url)


