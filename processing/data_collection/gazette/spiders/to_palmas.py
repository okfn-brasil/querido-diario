from dateparser import parse
import datetime as dt
import requests
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

last_page_number_xpath = '//div[@class="paginacao"]/ul[@class="pagination"]/li[last()-1]/a[last()]/text()'


class ToPalmasSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '1721000'
    name = 'to_palmas'
    allowed_domains = ['diariooficial.palmas.to.gov.br', 'legislativo.palmas.to.gov.br']
    to_palmas_url = 'http://diariooficial.palmas.to.gov.br/todos-diarios/?page={page_number}'
    start_urls = ['http://diariooficial.palmas.to.gov.br/todos-diarios/']

    def parse(self, response):
        """
        @url http://diariooficial.palmas.to.gov.br/todos-diarios/
        @returns requests 142
        """
        last_page_number_str = response.xpath(last_page_number_xpath).extract_first()
        last_page_number = int(last_page_number_str)
        for page_number in range(1, last_page_number + 1):
            url = self.to_palmas_url.format(page_number=page_number)
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        """
        @url http://diariooficial.palmas.to.gov.br/todos-diarios/?page=1
        @returns items 14
        """
        li_list = response.css('div.diario-content-todos > ul > li')
        for li in li_list:
            edicao, data = li.xpath('.//*[@id="audio-titulo"]/text()').re(
                r'(\d*)ª Edição de (.*$)'
            )
            url_edicao = li.xpath('.//*[@id="detalhes"]/a/@href').extract_first()
            abs_url = response.urljoin(url_edicao)
            pdf_url = requests.head(abs_url, allow_redirects=True).url
            data_publicacao = parse(data, languages=['pt']).date()
            gazette_object = self.create_gazette_object(
                date=data_publicacao, file_url=pdf_url, is_extra_edition=False
            )
            xpath_suplementos = li.xpath('.//*[@id="btn_baixar_titulo"]')
            for xpath_suplemento in xpath_suplementos:
                suplemento_url = xpath_suplemento.xpath('./@href').extract_first()
                suplemento_pdf_url = requests.get(
                    response.urljoin(suplemento_url), allow_redirects=True
                ).url
                # suplemento_nome = xpath_suplemento.xpath(
                #     './text()'
                # ).extract_first()
                gazette_object_extra = self.create_gazette_object(
                    date=data_publicacao,
                    file_url=suplemento_pdf_url,
                    is_extra_edition=True,
                )
                yield gazette_object_extra

            yield gazette_object

    def create_gazette_object(
        self, date, file_url, is_extra_edition=False, scraped_at=None, power='executive'
    ):
        if not scraped_at:
            scraped_at = dt.datetime.utcnow()
        file_urls = [file_url]
        gazette_object = Gazette(
            date=date,
            file_urls=file_urls,
            is_extra_edition=is_extra_edition,
            municipality_id=self.MUNICIPALITY_ID,
            scraped_at=scraped_at,
            power=power,
        )
        return gazette_object
