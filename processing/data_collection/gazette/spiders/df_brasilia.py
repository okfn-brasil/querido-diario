import re
import json
import itertools
import dateparser
import requests

from datetime import datetime
from scrapy import Request, Spider
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DfBrasiliaSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '5300108'
    GAZETTE_URL = 'http://dodf.df.gov.br/listar'

    MONTHS = [
        '12_Dezembro',
        '11_Novembro',
        '10_Outubro',
        '09_Setembro',
        '08_Agosto',
        '07_Julho',
        '06_Junho',
        '05_Maio',
        '04_Abril',
        '03_Março',
        '02_Fevereiro',
        '01_Janeiro'
    ]
    YEARS = ['2018', '2017', '2016', '2015']
    MONTHS_YEARS = itertools.product(MONTHS, YEARS)

    DATE_REGEX = r'.+\/DODF [0-9]+ ([0-9]{2}-[0-9]{2}-[0-9]{4})(.*)$'
    EXTRA_EDITION_TEXT = "EDICAO EXTR"
    PDF_URL = 'http://dodf.df.gov.br/index/visualizar-arquivo/?pasta={}&arquivo={}'

    allowed_domains = ['dodf.df.gov.br']
    name = 'df_brasilia'

    def start_requests(self):
        for month, year in self.MONTHS_YEARS:
            response = requests.get(f'{self.GAZETTE_URL}?dir={year}/{month}')
            days = response.json()['data']
            if not days:
                continue

            for day in days.values():
                yield Request(f'{self.GAZETTE_URL}?dir={year}/{month}/{day}')

    def parse(self, response):
        """
        @url http://dodf.df.gov.br/listar?dir={YEAR}/{MONTH}/{DAY}
        @returns items 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """
        json_response = json.loads(response.body_as_unicode())
        json_dir = json_response['dir']
        json_data = json_response['data']

        date = re.search(self.DATE_REGEX, json_dir).group(1)
        date = dateparser.parse(date)
        is_extra_edition = self.EXTRA_EDITION_TEXT in json_dir

        path = json_dir.replace('/', '|')
        file_urls = [self.PDF_URL.format(path, url.split('/')[-1]) for url in json_data]

        yield Gazette(
            date=date,
            file_urls=file_urls,
            is_extra_edition=is_extra_edition,
            municipality_id=self.MUNICIPALITY_ID,
            scraped_at=datetime.utcnow(),
            power='executive_legislative'
        )
