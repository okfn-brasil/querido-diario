from dateparser import parse
import datetime as dt
import re

import scrapy

from gazette.items import Gazette


class RsPontaGrossaSpider(scrapy.Spider):
    MUNICIPALITY_ID = '4119905'
    name = 'pr_ponta_grossa'
    allowed_domains = ['pontagrossa.pr.gov.br']
    start_urls = ['http://www.pontagrossa.pr.gov.br/diario-oficial/']

    def parse(self, response):
        """
        @url http://www.pontagrossa.pr.gov.br/diario-oficial/
        @returns requests 48
        """
        pdf_links = response.css(".view-content .field a::attr(href)").extract()
        for pdf in pdf_links:
            print(pdf)
            if "sem_atos" in pdf:
                continue
            pdf_link_info = re.search('.*/diario-oficial/_?(\d{4})-(\d{2})-(\d{2}).*.pdf', pdf)
            ano = pdf_link_info.group(1)
            mes = pdf_link_info.group(2)
            dia = pdf_link_info.group(3)
            print("ANO {0} MES {1} DIA {2} ".format(ano,mes,dia))


