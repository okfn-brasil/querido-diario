# -*- coding: utf-8 -*-
from dateparser import parse
import datetime as dt

import scrapy

from gazette.items import Gazette


class SpCampinas(scrapy.Spider):
    MUNICIPALITY_ID = '3509502'
    name = 'sp_campinas'
    allowed_domains = ['campinas.sp.gov.br']
    start_urls = ['http://www.campinas.sp.gov.br/diario-oficial/index.php']
    sp_campinas_url = 'http://www.campinas.sp.gov.br/'
    selector_url = 'http://www.campinas.sp.gov.br/diario-oficial/index.php?mes={}&ano={}'

    def parse(self, response):
        today = dt.date.today()
        next_year = today.year + 1
        for year in range(2018, next_year):
            for month in range(1, 13):
                if year == today.year and month > today.month:
                    continue
                url = self.selector_url.format(month, year)
                yield scrapy.Request(url, self.parse_month_page)


    def parse_month_page(self, response):
        items = []
        mesAno = response.css(".tabelaDiario:first-child tr th:nth-child(2)::text").extract_first()
        diarios = response.css(".tabelaDiario:first-child tr td a")
        for diario in diarios:
            link = diario.css('::attr(href)').extract_first().replace('../', '')
            dia = diario.css('::text').extract_first()
            date = parse(f'{dia} {mesAno}', languages=['pt']).date()
            url = f'{self.sp_campinas_url}{link}'
            # campinas does not have neither extra edition nor explicit power division (one pdf handles both)
            is_extra_edition = False
            power = 'executive'
            items.append(
                Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=is_extra_edition,
                    municipality_id=self.MUNICIPALITY_ID,
                    scraped_at=dt.datetime.utcnow(),
                    power=power
                )
            )
        return items
