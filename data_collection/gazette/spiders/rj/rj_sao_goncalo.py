import re
from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjSaoGoncaloSpider(BaseGazetteSpider):
    name = "rj_sao_goncalo"
    TERRITORY_ID = "3304904"
    allowed_domains = ["do.pmsg.rj.gov.br"]
    start_date = date(1998, 2, 3)
    BASE_URL = "https://do.pmsg.rj.gov.br/index?NumeroPagina={page}&Termo=a&DataInicial={raw_start_date}&DataFinal={raw_end_date}&PesquisarTermo=Pesquisar"

    def start_requests(self):
        yield scrapy.Request(self.format_base_url(1))

    def parse(self, response):
        for card in response.xpath("//div[@class='card mb-3']"):
            gazette = self.get_gazette_data(response, card)
            yield Gazette(
                date=gazette["date"],
                edition_number=gazette["edition_number"],
                file_urls=[gazette["url"]],
                is_extra_edition=gazette["is_extra"],
                power="executive",
            )

        current_page = int(re.search(r"NumeroPagina=(.*?)&", response.url).group(1))
        last_page_link = response.xpath(
            "//ul[@class='pagination pagination-sm']/a[last()]/font/text()"
        ).get()
        if last_page_link and int(last_page_link) > current_page:
            next_page = current_page + 1
            yield scrapy.Request(self.format_base_url(next_page))

    def get_gazette_data(self, response, card):
        gazette = {}
        card_header = card.xpath("div[@class='card-header']")

        gazette["date"] = self.get_date(card_header)
        gazette["edition_number"] = self.get_edition_number(card, gazette["date"])
        gazette["url"] = self.get_url(response, card_header)
        gazette["is_extra"] = "EXTRA" in card_header.get().upper()

        return gazette

    def get_date(self, card_header):
        raw_gazette_date = card_header.xpath(".//a/text()").get()
        return datetime.strptime(raw_gazette_date, "%d/%m/%Y").date()

    def get_edition_number(self, card, gazette_date):
        gazette_edition_number = ""
        # as edicoes comecaram a ser numeradas a partir de 18/08/2020
        if gazette_date >= date(2020, 8, 18):
            raw_card_body = (
                card.xpath("div[@class='card-body']")
                .get()
                .replace(".", "")
                .replace("°", "º")
            )
            match = re.search("Nº\s+(\w+)", raw_card_body)
            gazette_edition_number = "" if match is None else match.group(1)
        return gazette_edition_number

    def get_url(self, response, card_header):
        url_subdir = card_header.xpath(".//a/@href").get()
        year = re.search(r"/(.*?)_", url_subdir).group(1)
        # corrige url em edicoes que estao com link errado, ex: 21/01/2017
        if len(year) == 2:
            url_subdir = url_subdir.replace(f"/{year}_", f"/20{year}_")
        return response.urljoin(url_subdir)

    def format_base_url(self, page_number):
        return self.BASE_URL.format(
            page=page_number,
            raw_start_date=self.start_date.strftime("%Y-%m-%d"),
            raw_end_date=self.end_date.strftime("%Y-%m-%d"),
        )
