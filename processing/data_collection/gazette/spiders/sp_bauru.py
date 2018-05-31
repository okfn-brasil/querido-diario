import dateparser

from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

now = datetime.now()

class SpBauruSpider(BaseGazetteSpider):

    MUNICIPALITY_ID = '3506003'
    PAGES_URL = 'http://www.bauru.sp.gov.br/juridico/diariooficial.aspx?a={}m={}'
    PDF_URL = 'http://www.bauru.sp.gov.br{}'
    MONTHS = [str(x).zfill(2) for x in range(1,13)]
    YEARS = range(2015,now.year+1)

    DATE_CSS = 'main div.container ul ul ul li b::text'
    PDF_HREF_CSS = 'main div.container ul ul ul li a::attr(href)'

    allowed_domains = ['bauru.sp.gov.br']
    name = 'sp_bauru'
    start_urls = ['http://www.bauru.sp.gov.br/juridico/diariooficial.aspx']

    def date_parse(dates):
        for date in dates:
            dates[date] = dateparser.parse(dates[date][0:10],languages=['pt']).date()
        return dates

    def pdf_link(links):
        for link in links:
            links[link] = PDF_URL.format(links[link])
        return links

    for year in range(len(YEARS)):
        url = pdf_link(response.css(PDF_HREF_CSS).extract())
        date = date_parse(response.css(DATE_CSS).extract())

        for month in range(len(date)):
            yield Gazette(
                date=date[month],
                file_urls=[url][month],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive_legislature',
                scraped_at=datetime.utcnow(),
            )
