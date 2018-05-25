import re
import dateparser

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette

class GazetteElement:
    MUNICIPALITY_ID = '2304400'
    PDF_URL = 'http://apps.fortaleza.ce.gov.br/diariooficial/{}'

    def __init__(self, element):
        self.element = element

    def date(self):
        date_str = self.element.css('td:nth-child(2)::text').extract_first()
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


class CeFortalezaSpider(Spider):
    GAZETTE_ELEMENT_CSS = '.diarios-oficiais .table-responsive tbody tr'
    NEXT_PAGE_CSS = 'ul.pagination .page-link'

    allowed_domains = ['apps.fortaleza.ce.gov.br']
    name = 'ce_fortaleza'

    start_urls = []

    for year in range(2015, datetime.now().year):
        start_urls.append('http://apps.fortaleza.ce.gov.br/diariooficial/?num-diario=&content-diario=&ano-diario=' + str(year) + '&mes-diario=todos&current=1')

    def parse(self, response):
        """
        @url http://apps.fortaleza.ce.gov.br/diariooficial/
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ELEMENT_CSS):
           yield GazetteElement(element).to_gazette()

        next_link = response.css(self.NEXT_PAGE_CSS)

        if next_link:
            page_number = next_link[-1].css('.page-link::attr(href)').extract_first().split('#')[1]
            url = response.url.split('current')[0] + '&current=' + str(page_number)
            yield Request(url)
