import re
import dateparser
import w3lib.url

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette


class PrSaoJosePinhaisSpider(Spider):
    GAZETTE_ELEMENT_CSS = '.container-publicacao .item-publicacao'
    DATE_CSS = '.item-info::text'
    NEXT_PAGE_CSS = '.item-paginacao a::attr(href)'
    NEXT_PAGE_XPATH = '//div[@class="item-paginacao"]/a[last()]/text()'

    MUNICIPALITY_ID = '4125506'

    allowed_domains = ['diariooficial.sjp.pr.gov.br']
    name = 'pr_sao_jose_pinhais'
    start_urls = ['http://diariooficial.sjp.pr.gov.br/?nr_edicao=&ano_edicao=&entidade=12526&dt_publicacao_de=&dt_publicacao_ate=&resumo=']

    def parse(self, response):
        """
        @url http://diariooficial.sjp.pr.gov.br/
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        # for element in response.css(self.GAZETTE_ELEMENT_CSS):
        #     url = element.css('a::attr(href)').extract_first()
        #     date = dateparser.parse(element.css(self.DATE_CSS).extract()[2], languages=['pt']).date()
        #
        #     yield Gazette(
        #         date=date,
        #         file_urls=[url],
        #         is_extra_edition=False,
        #         municipality_id=self.MUNICIPALITY_ID,
        #         power='executive',
        #         scraped_at=datetime.utcnow(),
        #     )
        print(response.xpath(self.NEXT_PAGE_XPATH).extract())
        # for page_number in response.css(self.NEXT_PAGE_CSS).re('#(\d)+'):
        #     next_url = w3lib.url.add_or_replace_parameter(response.url, 'current', page_number)
        #     yield  Request(next_url)
