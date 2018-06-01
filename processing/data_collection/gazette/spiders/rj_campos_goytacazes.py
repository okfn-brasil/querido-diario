import re
import dateparser

from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

class RjCampoGoytacazesSpider(BaseGazetteSpider):
    GAZETTE_ELEMENT_CSS = 'ul.ul-licitacoes li'
    MUNICIPALITY_ID = '3301009'

    allowed_domains = ['www.campos.rj.gov.br']
    name = 'rj_campos_goytacazes'
    start_urls = ['https://www.campos.rj.gov.br/diario-oficial.php?PGpagina=1']

    def parse(self, response):
        """
        @url https://www.campos.rj.gov.br/diario-oficial.php?PGpagina=1
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            url = element.css('a::attr(href)').extract_first()
            gazette_text = element.css("h4::text").extract_first()
            date_text = gazette_text.split(' - ')[0].split('Eletrônico de ')[1]
            date = dateparser.parse(date_text, languages=['pt']).date()

            extra_edition = gazette_text.startswith('Suplemento')

            yield Gazette(
              date=date,
              file_urls=[url],
              is_extra_edition=extra_edition,
              municipality_id=self.MUNICIPALITY_ID,
              power='executive',
              scraped_at=datetime.utcnow(),
            )

        next_url = response.css('.pagination').xpath("//a[contains(text(), 'Proxima')]/@href").extract_first()

        if next_url:
            yield  Request(response.urljoin(next_url))
