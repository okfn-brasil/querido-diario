import dateparser
from scrapy import Request
from scrapy import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301702"
    PDF_URL = "http://duquedecaxias.rj.gov.br/portal/{}"

    GAZETTE_ELEMENT_CSS = "ul.jornal li"
    NEXT_PAGE_CSS = "ul.pagination li.next a::attr(href)"
    DATE_CSS = "span.article-date::text"
    EXTRA_EDITION_CSS = "span.edicao_extraordinaria::text"
    DATE_REGEX = r"([\d]+)[ |]+([\w]+)[ |]+([\d]+)"

    allowed_domains = ["duquedecaxias.rj.gov.br"]
    name = "rj_duque_de_caxias"
    start_urls = ["http://duquedecaxias.rj.gov.br/portal/boletim-oficial.html"]

    def parse(self, response):
        """
        @url http://duquedecaxias.rj.gov.br/portal/boletim-oficial.html
        @returns requests 1
        @scrapes date file_urls is_extra_edition power
        """

        #TODO: Criar dois tipos de parsers para o período de 2017 a ano_atual - 1 e anterior a 2017 (2013 a 2016)

        #self.logger.setLevel()
        for element in response.xpath('//div[contains(@class,"panel-body")]').getall():
            self.logger.info(element)
            pdf_marker = Selector(text=element).xpath('//i[contains(@class,"far fa-file-pdf")]').get()
            if pdf_marker is not None:
                raw_edition_number = Selector(text=element).xpath('string(//div//div[1])').get()
                raw_date = Selector(text=element).xpath('string(//div//div[2])').get()
                date = dateparser.parse(raw_date, languages=["pt"]).date()
                url = self.extract_url(Selector(text=element))

                self.logger.info("%s, %s, %s, %s", raw_edition_number, raw_date, date.strftime('%d/%m/%Y'),
                                 url)

                #TODO
                #is_extra_edition = self.extract_extra_edition_info(element)

                yield Gazette(
                    date=date,
                    file_urls=[url],
                    #is_extra_edition=is_extra_edition,
                    #edition_number=
                    power="executive_legislative",
                )

        #for url in response.css(self.NEXT_PAGE_CSS).extract():
        #    yield Request(url)


    def extract_url(self, element):
        path = element.css("a::attr(href)").extract_first()
        return self.PDF_URL.format(path)

    def extract_extra_edition_info(self, element):
        extra_edition_data = element.css(self.EXTRA_EDITION_CSS).extract_first()
        return extra_edition_data == "Edição Extraordinária"