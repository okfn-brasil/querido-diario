from dateparser import parse
from datetime import date, datetime
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrMaringaSpider(BaseGazetteSpider):
    TERRITORY_ID = '4115200'
    name = 'pr_maringa'
    allowed_domains = ['maringa.pr.gov.br']
    starting_year = 2015
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Content-Type':'application/x-www-form-urlencoded'
        }
    }

    def start_requests(self):
        """
        @url http://venus.maringa.pr.gov.br/arquivos/orgao_oficial/paginar_orgao_oficial_ano.php
        @returns requests 1
        """
        yield scrapy.FormRequest(
            'http://venus.maringa.pr.gov.br/arquivos/orgao_oficial/paginar_orgao_oficial_ano.php',
            formdata={
                'ano': '2018',
                'entrar': 'Buscar'
            },
            callback=self.parse_year
        )

    def parse_year(self, response):
        # print(response.body)
        yield Gazette(
            date=date(2018, 6, 6),
            file_urls=['http://venus.maringa.pr.gov.br/arquivos/orgao_oficial/arquivos/oom%202900.pdf'],
            is_extra_edition=True,
            territory_id=self.TERRITORY_ID,
            power='executive_legislature',
            scraped_at=datetime.utcnow()
        )
