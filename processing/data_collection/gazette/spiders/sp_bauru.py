import dateparser

from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

now = datetime.now()

class SpBauruSpider(BaseGazetteSpider):

    MUNICIPALITY_ID = '3506003'
    PDF_URL = 'http://www.bauru.sp.gov.br{}'

    BASE_URL, PAGE_URL = 'http://www.bauru.sp.gov.br/juridico/diariooficial.aspx?a={}m={}', []
    MONTHS = [str(x).zfill(2) for x in range(1,13)]

    # creating url for every month of every year
    for YEAR in range(2015,now.year+1):
        for ATUAL in range(12):
            if(ATUAL+1 > now.month and YEAR == now.year): break
            PAGE_URL.append(BASE_URL.format(YEAR,MONTHS[ATUAL]))


    DATE_CSS = 'b::text'
    PDF_HREF_CSS = 'a::attr(href)'
    GAZETTE_CSS = 'main div.container ul ul ul li'

    allowed_domains = ['bauru.sp.gov.br']
    name = 'sp_bauru'
    start_urls = [PAGE_URL[0]]

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

        for url in range(1,len(PAGE_URL))):
            yield Request(PAGE_URL[url])

    def extract_date(self, element):
        date = response.css(DATE_CSS).extract_first().split()
        return dateparser.parse(date[0]).date()

    def extract_url(self,element):
        href = element.css(self.PDF_HREF_CSS).extract_first()
        return self.PDF_URL.format(href)
