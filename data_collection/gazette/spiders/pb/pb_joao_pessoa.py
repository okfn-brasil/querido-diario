import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbJoaoPessoaSpider(BaseGazetteSpider):
    name = "pb_joao_pessoa"
    TERRITORY_ID = "2507507"
    start_date = datetime.date(2022, 3, 28)
    start_urls = ["https://www.joaopessoa.pb.gov.br/doe-jp/"]

    def parse(self, response):
        follow_next_page = True

        gazettes = response.css("h4.card-title")
        for gazette in gazettes:
            gazette_url = gazette.xpath(".//following-sibling::a/@href").get()
            edition_number = gazette.css("a::text").re_first(r"Edição (\d+\/\d+)")

            raw_gazette_date = gazette.css("a::text").re_first(r"(\d{2}\/\d{2}\/\d{4})")
            if not raw_gazette_date:
                continue

            gazette_date = datetime.datetime.strptime(
                raw_gazette_date, "%d/%m/%Y"
            ).date()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                power="executive_legislative",
            )

            if gazette_date < self.start_date:
                follow_next_page = False
                break

        next_page_url = response.css("a.next::attr(href)").get()
        if follow_next_page and next_page_url:
            yield scrapy.Request(next_page_url)
