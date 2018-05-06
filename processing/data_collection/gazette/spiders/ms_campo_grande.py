# -*- coding: utf-8 -*-
from dateparser import parse
import datetime as dt

import scrapy

from gazette.items import Gazette


class MsCampoGrandeSpider(scrapy.Spider):
    MUNICIPALITY_ID = '5002704'
    name = 'ms_campo_grande'
    allowed_domains = ['portal.capital.ms.gov.br']
    start_urls = ['http://portal.capital.ms.gov.br/diogrande/diarioOficial']
    ms_campo_grande_url = 'http://portal.capital.ms.gov.br/diogrande/diarioOficial'

    def parse(self, response):
        """
        @url http://portal.capital.ms.gov.br/diogrande/diarioOficial
        @returns requests 4
        """
        today = dt.date.today()
        next_year = today.year + 1
        for year in range(2015, next_year):
            for month in range(1, 13):
                if year == today.year and month > today.month:
                    return

                yield scrapy.FormRequest(
                    url=self.ms_campo_grande_url,
                    callback=self.parse_month_page,
                    method='POST',
                    formdata={
                        'mes': str(month),
                        'ano': str(year)
                    }
                )

    def parse_month_page(self, response):
        """
        @url http://portal.capital.ms.gov.br/diogrande/diarioOficial
        @returns items 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """
        items = []
        year = response.css('#leftToRight > h3').extract_first().split('/')[1]  # "2018"
        docs = response.css(".arquivos li")
        for doc in docs:
            url = doc.css('.inner-detail a::attr(href)').extract_first()
            day = doc.css('.day strong::text').extract_first()
            month = doc.css('.month::text').extract_first()
            date = parse(f'{day}/{month}/{year}', languages=['pt']).date()
            is_extra_edition = 'Edição Extra' in doc.css('.inner-detail a p:last-child::text')
            power = 'executive_legislature'
            items.append(
                Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=is_extra_edition,
                    municipality_id=self.MUNICIPALITY_ID,
                    power=power,
                    scraped_at=dt.datetime.utcnow(),
                )
            )
        return items
