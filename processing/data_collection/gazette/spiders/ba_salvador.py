# -*- coding: utf-8 -*-
import datetime
import urllib.parse

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaSalvadorSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '2927408'
    name = 'ba_salvador'
    allowed_domains = ['salvador.ba.gov.br']
    power = 'executive'

    def start_requests(self):
        # According to their website, they have gazettes available from 2001-01-01
        initial_search_parameters = {
            'filterDateFrom': '2001-01-01',
            'filterDateTo': datetime.date.today().strftime('%Y-%m-%d'),
            'option': 'com_dmarticlesfilter',
            'view': 'articles',
            'Itemid': '3',
            'userSearch': '1',
            'limstart': '0',
            'limitstart': '10'
        }
        encoded_params = urllib.parse.urlencode(initial_search_parameters)
        base_url = 'http://www.dom.salvador.ba.gov.br/index.php'
        first_page_url = f'{base_url}?{encoded_params}'
        yield scrapy.Request(first_page_url)

    def parse(self, response):
        months = [
            'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
            'agosto', 'setembro', 'outubro', 'novembro', 'dezembro',
        ]
        for gazette in response.css('.dmarticlesfilter_results_title'):
            gazette_id = gazette.re_first('DOM-([\d]+)')
            gazette_date = gazette.css(
                '#dmarticlesfilter_results_date::text').extract_first('')

            parsed_date = dateparser.parse(gazette_date, settings={'DATE_ORDER': 'YMD'})
            month = months[parsed_date.month - 1]
            full_date = parsed_date.strftime('%d-%m-%Y')

            pdf_url = f'http://www.dom.salvador.ba.gov.br/' \
                f'images/stories/pdf/{parsed_date.year}/{month}/dom-{gazette_id}-{full_date}.pdf'

            yield Gazette(
                date=parsed_date.date(),
                file_urls=[pdf_url, ],
                municipality_id=self.MUNICIPALITY_ID,
                power=self.power,
                scraped_at=datetime.datetime.utcnow(),
            )

        for href in response.css('.paginacao a::attr(href)'):
            yield response.follow(href, callback=self.parse)
