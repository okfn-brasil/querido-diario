import datetime
import scrapy
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MtRondonopolisSpider(BaseGazetteSpider):
    TERRITORY_ID = "5107602"
    name = "mt_rondonopolis"
    allowed_domains = ["rondonopolis.mt.gov.br"]
    start_urls = ["http://www.rondonopolis.mt.gov.br/diario-oficial/"]

    start_date = datetime.date(2004, 9, 1)

    # o diario vai ate a pagina 238
    # a data mais antiga é 01/09/2004 ; edicao 852
    # data transiçao para pdf 29/06/11

    def parse(self, response):
        to_next = True
        for gazette in response.css("tbody tr"):    
            date = gazette.xpath('td[contains(text(), "/")]//text()').get()
            parsed_date = datetime.datetime.strptime(date, "%d/%m/%y").date()

            if self.start_date > parsed_date:
                to_next = False
                break

            edition = gazette.css("td:first-child::text").get()
            pdf_url = response.urljoin(gazette.css("td a::attr(href)").get())

            yield Gazette(
                file_urls=[pdf_url],
                date=parsed_date,
                power="executive",
                is_extra_edition=False,
                edition_number=edition,
            )

        if to_next:
            next_page = response.xpath(
                '//li[@class="page-item"]/a[contains(text(), "Próxima")]//@href'
            ).get()
            yield scrapy.Request(f'http://www.rondonopolis.mt.gov.br/diario-oficial/{next_page}')