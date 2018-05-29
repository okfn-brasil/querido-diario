# -*- coding: utf-8 -*-
from dateparser import parse
import datetime as dt
import scrapy
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaFeiraDeSantanaSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '2910800'
    name = 'ba_feira_de_santana'
    allowed_domains = ['diariooficial.feiradesantana.ba.gov.br']
    start_urls = ['http://www.diariooficial.feiradesantana.ba.gov.br']
    powers = {'executive': 1, 'legislative': 2}
    last_page = 1

    def parse(self, response):
        """
        @url http://www.diariooficial.feiradesantana.ba.gov.br/?p=29
        @returns requests 30
        """
        gazette_table = response.css('.style166')
        gazettes_links = gazette_table.xpath('a//@href').extract()
        dates = gazette_table.css('a::text').extract()

        for url, date in zip(gazettes_links, dates):
            edition = self._extract_edition(url)
            power = self._extract_power(url)
            power_id = self.powers[power]

            gazette = Gazette(
                date=parse(date, languages=['pt']).date(),
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power=power,
                scraped_at=dt.datetime.utcnow(),
            )

            gazette_details_page = f'abrir.asp?edi={edition}&p={power_id}'
            gazette_url = response.urljoin(gazette_details_page)
            gazette_request = Request(gazette_url, self.parse_document_url)
            gazette_request.meta['item'] = gazette

            yield gazette_request

        current_page_selector = '#pages ul li.current::text'
        current_page = response.css(current_page_selector).extract_first()
        next_page = int(current_page) + 1
        next_page_url = response.urljoin(f'/?p={next_page}')

        if next_page > self.last_page:
            self.last_page = next_page
            yield Request(next_page_url)

    def parse_document_url(self, response):
        partial_url = response.css('iframe::attr(src)').extract_first()
        document_url = response.urljoin(partial_url)
        item = response.meta['item']
        item['file_urls'] = [document_url]
        return item

    def _extract_power(self, url):
        if url.find('st=1') != -1:
            return 'executive'
        return 'legislative'

    def _extract_edition(self, url):
        edition_index = url.find('edicao=') + len('edicao=')
        edition = url[edition_index:]
        return edition
