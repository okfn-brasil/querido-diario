# -*- coding: utf-8 -*-
import scrapy
import datetime as dt

from gazette.items import Gazette

class MgBelohorizonteSpider(scrapy.Spider):
    MUNICIPALITY_ID = 3106200
    name = 'mg_belohorizonte'
    allowed_domains = ['portal6.pbh.gov.br']
    start_urls = ['http://portal6.pbh.gov.br/dom/iniciaEdicao.do?method=DomDia']
    mg_belohorizonte_url = 'http://portal6.pbh.gov.br/'
    documents_url = 'http://portal6.pbh.gov.br/dom/iniciaEdicao.do?method=DomDia&dia={}&comboAno={}'
    
    # http://portal6.pbh.gov.br/dom/iniciaEdicao.do?method=DomDia&dia=01/01/2018&comboAno=2018
    # response.xpath('//p[contains(@class,"dom-chamadas")]/a/@href').extract_first()

    def parse(self, response):
        
        start_date = dt.date(2016, 7, 5)
        delta = dt.timedelta(days=1)
        while start_date <= dt.date.today():
            url = self.documents_url.format(start_date.strftime('%d/%m/%Y'), start_date.year)
            print('----------'+url+'---------')
            yield scrapy.Request(url, self.parse_details)
            start_date += delta

    def parse_pagelink(self,response):
        url = response.xpath('//p[contains(@class,"dom-chamadas")]/a/@href').extract_first()
        if url not None:
            url = response.urljoin(url)

    
    
    def parse_details(self, response):
        file_url = response.xpath('//a[contains(@alt, "link_anexo")]/@href').extract_first()        
        items = []
        if file_url is not None:
            power = 'executive_legislature'
            items.append(
                Gazette(
                    date=date,
                    file_urls=[self.mg_belohorizonte_url + file_url],
                    is_extra_edition=False,
                    municipality_id=self.MUNICIPALITY_ID,
                    power=power,
                    scraped_at=dt.datetime.utcnow(),
                )
            )
        return items
