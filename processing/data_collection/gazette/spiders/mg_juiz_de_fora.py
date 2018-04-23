from dateparser import parse
import datetime as dt

import scrapy

from gazette.items import Gazette


class MgJuizDeForaSpider(scrapy.Spider):
    MUNICIPALITY_ID = '3136702'
    name = 'mg_juiz_de_fora'
    allowed_domains = ['www.pjf.mg.gov.br']
    start_urls = ['https://www.pjf.mg.gov.br/secretarias/cpl/editais/resultados/2018/janeiro/index.php']

    BASE_URL = 'https://www.pjf.mg.gov.br/secretarias/cpl/editais/resultados/'
    MONTHS = ['janeiro','fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho',
              'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

    def parse(self, response):
        """
        @url https://www.pjf.mg.gov.br/secretarias/cpl/editais/resultados/2018/janeiro/index.php
        @returns
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """
        current_year = dt.date.today().year + 1
        for year in range(2017, current_year):
            for month in self.MONTHS:
                current_url = self.BASE_URL + str(year) + '/' + str(month) + '/index.php'
                yield scrapy.Request(current_url, self.parse_year_month_page)

    def parse_year_month_page(self, response):
        """
        @url https://www.pjf.mg.gov.br/secretarias/cpl/editais/resultados/2018/janeiro/index.php
        @returns
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """
        gazette_table = response.css('.table-condensed')

        for gazette_node in gazette_table.css('tbody tr'):
            if len(gazette_node.css('td::text')) == 6:
                url = response.request.url.replace('/index.php', '/') + str(gazette_node.css('a::attr(href)').extract_first())
                date = gazette_node.css('td::text')[0].extract()
                date = parse(date, languages=['pt']).date()

                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=False,
                    municipality_id=self.MUNICIPALITY_ID,
                    power='executive',
                    scraped_at=dt.datetime.utcnow(),
                )