import datetime as dt
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
import scrapy
import re

class MaAcailandia(BaseGazetteSpider):
    TERRITORY_ID = "2100055"
    BASE_URL = "https://www.acailandia.ma.gov.br/"
    start_date = dt.date(2015, 12, 1)
    name = "ma_acailandia"
    allowed_domains = ["acailandia.ma.gov.br"]

    """
    NOT_EXTRA_EDITION_REGEX : regex pattern
        Used to filter if a string has only numbers. 
        Extra edition has a letter in the edition_code. 
        Example normal edition: 1235
        Example extra edition: 1235-A

    GAZETTE_EDITION_CODES: set of edition codes
        Used to not repeat gazettes in extraction.

    CATEGORY: string
        Used to filter Gazettes by subcategories of power. 
        Set to '' to get the Gazettes of all available powers.
        Categories range from 4 to 166 and do not follow a numerical pattern.
        Some of categories available:
            Buscar em todos as categorias = ''
            Assessoria de Comunicação = '23'
            Outras Publicações = '133'
            ...
    """

    NOT_EXTRA_EDITION_REGEX = re.compile(r'^([\s\d]+)$')
    GAZETTE_EDITION_CODES = set()
    CATEGORY = ''

    

    def start_requests(self):
        """Request a page that contains the number of pages between certain dates"""
        self.GAZETTE_EDITION_CODES = set()
        start = self.start_date.strftime('%d-%m-%Y').replace('-', '%2F')
        end = self.end_date.strftime('%d-%m-%Y').replace('-', '%2F')
        url = f'{self.BASE_URL}diariooficial/edicoes?categoria={self.CATEGORY}&data_inicial={start}&data_final={end}&t=titulo'
        yield scrapy.Request(
            url, 
            cb_kwargs=dict(url=url), 
        )

    def get_num_pages(self, response):
        """"Gets the number of pages in pagination"""
        pagination_items = response.xpath('//ul[@class="pagination"]/li/node()/text()').getall()
        if not pagination_items:
            return 1
        return int(pagination_items[-2])


    def parse_page(self, response):
        """"Parse items in a page into Gazettes without repeat edition(same pdf)"""
        items = response.xpath('//div[@class="col-md-12 list-publicacoes-diario"]/a/ul/li[contains(.,"Página")]//text()').getall()
        for item in items:
            splitted = item.split(' ')
            edition = splitted[3]
            if edition in self.GAZETTE_EDITION_CODES:
                self.logger.info(f'Skipping duplicate edition: {edition}')
                continue
            date = dt.datetime.strptime(splitted[5], '%d/%m/%Y').date()
            self.GAZETTE_EDITION_CODES.add(edition)
            download_url = f'{self.BASE_URL}diariooficial/getFile/{edition}'
            is_extra_edition = not self.NOT_EXTRA_EDITION_REGEX.match(edition)
            yield Gazette(
                date=date,
                file_urls = [download_url],
                edition_number = edition,
                is_extra_edition = is_extra_edition,
                territory_id = self.TERRITORY_ID,
                power = "executive_legislative",
            )

    def parse(self, response, url):
        """"Request all available pages and send to parser_page"""
        num_pages = self.get_num_pages(response)
        for page in range(1, num_pages  + 1):
            page_url = f'{url}&page={page}'
            yield scrapy.Request(
                page_url,
                callback=self.parse_page,
            )
    
    def closed(self, reason):
        del self.GAZETTE_EDITION_CODES
