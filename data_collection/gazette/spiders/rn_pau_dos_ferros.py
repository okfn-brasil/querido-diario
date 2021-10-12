import datetime
import logging

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnPauDosFerrosSpider(BaseGazetteSpider):
    name = "rn_pau_dos_ferros"
    allowed_domains = ["paudosferros.rn.gov.br"]
    start_date = datetime.date(2017, 1, 2)
    TERRITORY_ID = "2409407"
    start_urls = ["https://paudosferros.rn.gov.br/publicacoes.php"]

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response, page=0):
        gazettes = response.css('.list-group-item')
        last_page_number_css = '.pagination > li:nth-last-child(-n+2) > a > span::text'
        last_page_number = int(response.css(last_page_number_css).extract_first())
        follow_next_page = True

        for gazette in gazettes:
            gazette_date_raw = gazette.css('div > div > span::text').extract_first().strip()

            gazette_date = dateparser.parse(gazette_date_raw, languages=["pt"]).date()

            if gazette_date < self.start_date:
                follow_next_page = False
                break

            partial_url = gazette.css('a::attr(href)').extract_first()
            url = f"https://paudosferros.rn.gov.br/{partial_url}"

            yield Gazette(
                date=gazette_date,
                file_urls=[url],
                is_extra_edition=False,
                power="legislative",
            )

        next_page = page + 1
        if follow_next_page and next_page <= last_page_number:
            yield Request(
                f"https://paudosferros.rn.gov.br/publicacoes.php?pagina={next_page}", 
                cb_kwargs={"page": next_page}
            )

    # def parse(self, response):
    #     last_page_number_css = ".pagination > li:nth-child(5) > a > span::text"
    #     last_page_number = int(response.css(last_page_number_css).extract_first())
    #
    #     for page_number in range(0, last_page_number):
    #         yield Request(
    #             f"{self.start_urls[0]}?pagina={page_number}",
    #             callback=self.parse_gazette,
    #         )
    #
    # def parse_gazette(self, response):
    #
    #     for element in response.css('#lei > div'):
    #         date = parse(
    #             element.css('a > div > div > span::text').extract_first(), languages=["pt"]
    #         ).date()
    #
    #         if gazette_date < self.start_date:
    #             follow_next_page = False
    #             break
    #
    #         partial_url = element.css('a::attr(href)').extract_first()
    #
    #         url = f"{self.start_urls[0]}/{partial_url}"
    #
    #         yield Gazette(
    #             date=date,
    #             file_urls=[url],
    #             is_extra_edition=False,
    #             power="executive",
    #         )
