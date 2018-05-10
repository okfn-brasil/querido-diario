# -*- coding: utf-8 -*-
import scrapy
import datetime as dt
import re
from gazette.items import Gazette


class MgUberlandiaSpider(scrapy.Spider):
    MUNICIPALITY_ID = 3170206
    name = 'mg_uberlandia'
    allowed_domains = ['uberlandia.mg.gov.br']
    start_urls = ['http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=2535']
    urls = [
        'http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=2649',
        'http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=2779',
        'http://www.uberlandia.mg.gov.br/?pagina=Conteudo&id=3035',
    ]

    def parse(self, response):
        for url in self.urls:
            yield scrapy.Request(url, self.parse_year)

    def parse_year(self, response):
        url_months = self.links_months(response)
        for url in url_months:
            yield scrapy.Request(url, self.parse_month)

    def parse_month(self, response):
        url_issues = response.xpath('//a[contains(@href,"http://www.uberlandia.mg.gov.br/uploads")]')
        dates = self.list_dates(response)
        items = []

        for i, url in enumerate(url_issues):
            url_issue = url.xpath('@href').extract_first()
            power = 'executive_legislature'
            try:
                date = dt.datetime.strptime(dates[i], '%d/%m/%Y')
            except:
                date = None
            items.append(
                Gazette(
                    date=date,
                    file_urls=[url_issue],
                    is_extra_edition=False,
                    municipality_id=self.MUNICIPALITY_ID,
                    power=power,
                    scraped_at=dt.datetime.utcnow(),
                )
            )
        return items

    def links_months(self, response):
        variants = ['//div[contains(@class,"colunaConteudo")]/p/strong/span/span/a/@href',
                    '//div[contains(@class,"colunaConteudo")]/p/strong/span/span/span/a/@href',
                    '//div[contains(@class,"colunaConteudo")]/p/strong/a/@href',
                    '//div[contains(@class,"colunaConteudo")]/p/a/@href',
                    '//div[contains(@class,"colunaConteudo")]/p/span/span/strong/a/@href',
                    '//div[contains(@class,"colunaConteudo")]/p/span/span/span/a/@href',
                    ]
        urls = []
        for v in variants:
            url = response.xpath(v).extract()
            if len(url) > 0:
                for u in url:
                    urls.append(u)
        return urls

    def list_dates(self, response):
        dt1 = response.xpath('//p/span/text()').extract()
        dt2 = response.xpath('//p/text()').extract()
        dates = []
        for dt in dt1:
            d = re.findall('\d{2}/\d{2}/\d{4}', dt)
            if len(d) == 1:
                dates.append(d[0])

        for dt in dt2:
            d = re.findall('\d{2}/\d{2}/\d{4}', dt)
            if len(d) == 1:
                dates.append(d[0])

        return sorted(dates, reverse=True)
