from dateparser import parse
import datetime as dt
import re

import scrapy

from gazette.items import Gazette

class PrPontaGrossaSpider(scrapy.Spider):
    MUNICIPALITY_ID = '4119905'
    name = 'pr_ponta_grossa'
    allowed_domains = ['pontagrossa.pr.gov.br']
    start_urls = ['http://www.pontagrossa.pr.gov.br/diario-oficial/']
    ano_minimo = 2015

    def parse(self, response):
        """
        @url http://www.pontagrossa.pr.gov.br/diario-oficial/
        @returns requests 48
        """
        self.scrape_page(response)

    def scrape_page(self, response):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        pdf_links = response.css(".view-content .field a")

        pdf_infos = []
        for pdf_link in pdf_links:
            pdf_file_name = pdf_link.css("::attr(href)").extract_first()
            pdf_link_text = pdf_link.css("::text").extract_first()
            print(pdf_file_name)
            if "sem_atos" in pdf_file_name:
                continue
            pdf_link_info = re.search('.*/diario-oficial/_?(\d{4})-(\d{2})-(\d{2}).*.pdf', pdf_file_name)
            ano = int(pdf_link_info.group(1))
            if ano < self.ano_minimo:
                continue
            mes = pdf_link_info.group(2)
            dia = pdf_link_info.group(3)
        #is_extra = True#Dapaende do texto
            pdf_infos.append({ "ano" : ano, "mes" : mes, "dia":dia, "url": pdf_file_name })
        menor_ano_da_pagina =  min(map(lambda p: p.ano, pdf_infos))
        print(menor_ano_da_pagina)
        #if menor_ano_da_pagina >= self.ano_minimo:
        #    next_page_url = response.css(".pager-next::attr(href)").extract_first()
        #    yield scrapy.Request(next_page_url, self.scrape_page)

        #for pdf_info in pdf_infos:
        #    print(pdf_info.url)

