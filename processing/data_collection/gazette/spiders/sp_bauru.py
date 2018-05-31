import dateparser
import itertools

from itertools import product
from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

class SpBauruSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '3506003'

    MONTHS = [str(x).zfill(2) for x in range(1, 13)]
    YEARS = ['2015', '2016', '2017', '2018']
    MONTHS_YEARS = itertools.product(MONTHS, YEARS)

    BASE_URL = 'http://www.bauru.sp.gov.br{}'
    PAGE_URL = 'http://www.bauru.sp.gov.br/juridico/diariooficial.aspx?a={}&m={}'
    DATE_CSS = 'b::text'
    PDF_HREF_CSS = 'a::attr(href)'
    GAZETTE_CSS = 'main div.container ul ul ul li'

    allowed_domains = ['bauru.sp.gov.br']
    name = 'sp_bauru'

    def start_requests(self):
        for month, year in self.MONTHS_YEARS:
            yield Request(self.PAGE_URL.format(year, month))

    def parse(self, response):


        """
        @url http://www.bauru.sp.gov.br/juridico/diariooficial.aspx?a=2015m=01
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_CSS):
            url = self.extract_url(element)
            date = self.extract_date(element)

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive_legislature',
                scraped_at=datetime.utcnow(),
            )

    def extract_date(self, element):
        date = element.css(self.DATE_CSS).extract_first().split()
        return dateparser.parse(date[0]).date()

    def extract_url(self,element):
        href = element.css(self.PDF_HREF_CSS).extract_first()
        return self.BASE_URL.format(href)
