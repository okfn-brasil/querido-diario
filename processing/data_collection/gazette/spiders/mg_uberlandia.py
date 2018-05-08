# -*- coding: utf-8 -*-
import scrapy
import datetime as dt

from gazette.items import Gazette

class MgUberlandiaSpider(scrapy.Spider):
    MUNICIPALITY_ID = 3170206
    name = 'mg_uberlandia'
    allowed_domains = ['uberlandia.mg.gov.br']
    start_urls = ['http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=2535']
    urls = ['http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=2535',
            'http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=2649',
            'http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=2779',
            'http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=3035',
        ]
    
    def parse(self, response):

        for url in self.urls:
            yield scrapy.Request(url, self.parse_year)

    
    def parse_year(self, response):
        url_months = response.xpath('//a[contains(@target,"_blank") and contains(@href,"http://www.uberlandia.mg.gov.br")]')
        for url in url_months:
            url_month = url.xpath('@href').extract_first()
            yield scrapy.Request(url_month, self.parse_month)
            

    def parse_month(self,response):
        url_issues = response.xpath('//a[contains(@href,"http://www.uberlandia.mg.gov.br/uploads")]')
        items = []
        for url in url_issues:
            url_issue = url.xpath('@href').extract_first()
            power = 'executive_legislature'
            items.append(
                Gazette(
                    date=dt.date(2018, 5, 5), # temporário
                    file_urls=[url_issue],
                    is_extra_edition=False,
                    municipality_id=self.MUNICIPALITY_ID,
                    power=power,
                    scraped_at=dt.datetime.utcnow(),
                )
            )
        return items
