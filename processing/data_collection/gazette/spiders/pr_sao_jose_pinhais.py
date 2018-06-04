import re
import dateparser
import w3lib.url

from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

class PrSaoJosePinhaisSpider(BaseGazetteSpider):
    GAZETTE_ELEMENT_CSS = '.container-publicacao .item-publicacao'
    DATE_CSS = '.item-info::text'
    NEXT_PAGE_CSS = '.item-paginacao a:last-child::attr(href)'

    TERRITORY_ID = '4125506'

    allowed_domains = ['diariooficial.sjp.pr.gov.br']
    name = 'pr_sao_jose_pinhais'
    start_urls = ['http://diariooficial.sjp.pr.gov.br/?ano_edicao=&entidade=12526&pg=1']

    def parse(self, response):
        """
        @url http://diariooficial.sjp.pr.gov.br/?ano_edicao=&entidade=12526&pg=1
        @returns requests 1
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            url = element.css('a::attr(href)').extract_first()
            date = dateparser.parse(element.css(self.DATE_CSS).extract()[2], languages=['pt']).date()

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                power='executive',
                scraped_at=datetime.utcnow(),
            )

        current_page = w3lib.url.url_query_parameter(response.url, "pg")

        if not response.css(self.NEXT_PAGE_CSS).extract_first().endswith('pg=' + current_page):
            next_url = w3lib.url.add_or_replace_parameter(response.url, 'pg', str(int(current_page) + 1))
            yield  Request(next_url)
