from dateparser import parse
import datetime as dt

import scrapy
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMossoroSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '2408003'
    PDF_URL = 'https://www.prefeiturademossoro.com.br/jom/{}'

    GAZETTES_CSS = 'body > div > table:first-child > tr > td > table:last-child > tr > td > div > table > tr > td'
    PDF_INFO_CSS = 'td.TextoLink'
    PDF_REALTIVE_PATH_CSS = 'a::attr(href)'
    DATE_REGEX = r'[0-9]{1,2} de [A-Za-z].* de [0-9]{4}'
    IS_EXTRA_REGEX = r'-[A-Za-z]'

    allowed_domains = ['prefeiturademossoro.com.br']
    name = 'rn_mossoro'
    start_urls = ['https://www.prefeiturademossoro.com.br/jom/alljoms.php']

    def parse(self, response):
        dates = set()
        for element in response.css(self.GAZETTES_CSS):
            url = self.extract_url(element)
            date = self.extract_date(element)
            if url and date and date not in dates:
                dates.add(date)
                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=self.is_extra_edition(element),
                    municipality_id=self.MUNICIPALITY_ID,
                    power='executive_legislature',
                    scraped_at=dt.datetime.utcnow(),
                )

    def extract_url(self, element):
        realtive_path = element.css(self.PDF_REALTIVE_PATH_CSS).extract_first()
        if not realtive_path:
            return None

        return self.PDF_URL.format(realtive_path)

    def extract_date(self, element):
        date = element.css(self.PDF_INFO_CSS).re(self.DATE_REGEX)
        if not date:
            return None

        return parse(date[0], languages=['pt']).date()

    def is_extra_edition(self, element):
        return bool(element.css(self.PDF_INFO_CSS).re(self.IS_EXTRA_REGEX))
