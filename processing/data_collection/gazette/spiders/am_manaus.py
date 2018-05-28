import dateparser

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AmManausSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '1302603'
    GAZETTE_URL = 'http://dom.manaus.am.gov.br/diario-oficial-de-manaus'
    PAGE_URL = GAZETTE_URL + '/atct_topic_view?b_start:int={}&-C='

    EXTRA_EDITION_TEXT = 'Edição Extra'
    DATE_CSS = 'td:first-child span::text'
    GAZETTE_ROW_CSS = 'table.listing tbody tr'
    PDF_HREF_CSS = 'td:nth-child(2) a::attr(href)'
    PDF_TEXT_CSS = 'td:nth-child(2) a:last-child::text'

    SECOND_PAGE = 20
    LAST_PAGE = 1000
    STEP = 20

    allowed_domains = ['manaus.am.gov.br']
    name = 'am_manaus'
    start_urls = [GAZETTE_URL]

    def parse(self, response):
        """
        @url http://dom.manaus.am.gov.br/diario-oficial-de-manaus
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ROW_CSS):
            url = element.css(self.PDF_HREF_CSS).extract_first()
            date = dateparser.parse(
                element.css(self.DATE_CSS).extract_first(),
                languages=['pt']
            ).date()
            text = element.css(self.PDF_TEXT_CSS).extract_first()
            is_extra_edition = self.EXTRA_EDITION_TEXT in text

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive',
                scraped_at=datetime.utcnow(),
            )

        for index in range(self.SECOND_PAGE, self.LAST_PAGE, self.STEP):
            yield Request(self.PAGE_URL.format(index))
