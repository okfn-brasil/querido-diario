import dateparser

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PiTeresinaSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '2211001'

    ATTACHMENT_CSS = 'td:last-child a::attr(href)'
    DATE_CSS = 'td:nth-child(2)::text'
    GAZETTE_ROW_CSS = '.table tbody tr'
    NEXT_PAGE_CSS = '.box-paginacao a.paginacao:last-child::attr(href)'
    PDF_HREF_CSS = 'td:nth-child(3) a::attr(href)'

    allowed_domains = ['www.dom.teresina.pi.gov.br']
    name = 'pi_teresina'
    start_urls = ['http://www.dom.teresina.pi.gov.br/lista_diario.php']

    def parse(self, response):
        """
        @url http://www.dom.teresina.pi.gov.br/lista_diario.php
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ROW_CSS):
            gazette_url = element.css(self.PDF_HREF_CSS).extract_first()
            attachment_url = element.css(self.ATTACHMENT_CSS).extract_first()
            file_urls = list(filter(None, [gazette_url, attachment_url]))
            date = dateparser.parse(
                element.css(self.DATE_CSS).extract_first(),
                languages=['pt']
            ).date()

            yield Gazette(
                date=date,
                file_urls=file_urls,
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive',
                scraped_at=datetime.utcnow(),
            )

        next_page_url = response.css(self.NEXT_PAGE_CSS).extract_first()
        yield Request(response.urljoin(next_page_url))
