import re
import dateparser
import w3lib.url

from datetime import datetime
from scrapy import Request, FormRequest
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnNatalSpider(BaseGazetteSpider):
    GAZETTE_ELEMENT_CSS = '#texto a'
    MUNICIPALITY_ID = '2408102'

    allowed_domains = ['www.natal.rn.gov.br']
    name = 'rn_natal'

    def start_requests(self):
        base_url = 'http://www.natal.rn.gov.br/dom/'

        for year in range(2003, datetime.now().year + 1):
            for month in range(1, 13):
                print([year, month])
                data = dict(ano=str(year), mes=str(month), list='Listar')
                yield FormRequest(url=base_url, formdata=data, callback=self.parse)

    def parse(self, response):
        """
        @url http://www.natal.rn.gov.br/dom/
        @returns items 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            url = response.urljoin(element.css('::attr(href)').extract_first())
            link_text = element.css('::text').extract_first()
            date = dateparser.parse(link_text.split(' - ')[-1], languages=['pt']).date()
            extra_edition = ("Extra" in link_text)

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=extra_edition,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive',
                scraped_at=datetime.utcnow()
            )
