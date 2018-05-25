import re
import dateparser

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette

PDF_URL = 'http://apps.fortaleza.ce.gov.br/diariooficial/{}'

def generate_urls_by_year():
    urls = []
    for year in range(2015, datetime.now().year):
        urls.append(PDF_URL.format('?num-diario=&content-diario=&ano-diario=' + str(year) + '&mes-diario=todos&current=1'))

    return urls

class CeFortalezaSpider(Spider):
    DATE_CSS = 'td:nth-child(2)::text'
    GAZETTE_ELEMENT_CSS = '.diarios-oficiais .table-responsive tbody tr'
    NEXT_PAGE_CSS = 'ul.pagination .page-link'
    NEXT_PAGE_LINK_CSS = '.page-link::attr(href)'

    MUNICIPALITY_ID = '2304400'

    allowed_domains = ['apps.fortaleza.ce.gov.br']
    name = 'ce_fortaleza'

    start_urls = generate_urls_by_year()

    def parse(self, response):
        """
        @url http://apps.fortaleza.ce.gov.br/diariooficial/
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            url = self.extract_url(element)
            date = self.extract_date(element)

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive',
                scraped_at=datetime.utcnow(),
            )

        next_link = response.css(self.NEXT_PAGE_CSS)

        if next_link:
            page_number = next_link[-1].css(self.NEXT_PAGE_LINK_CSS).extract_first().split('#')[1]
            url = response.url.split('&current')[0] + '&current=' + str(page_number)
            yield Request(url)

    def extract_url(self, element):
        path = element.css('a::attr(href)').extract_first()
        return PDF_URL.format(path)

    def extract_date(self, element):
        date_str = element.css(self.DATE_CSS).extract_first()
        return dateparser.parse(date_str, languages=['pt']).date()
