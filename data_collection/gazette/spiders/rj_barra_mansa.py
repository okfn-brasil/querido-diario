import re
import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjBarraMansaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3300407"
    allowed_domains = ["barramansa.rj.gov.br"]
    name = "rj_barra_mansa"
    start_urls = [
        "https://portaltransparencia.barramansa.rj.gov.br/boletim-oficial/"
    ]
    start_date = "2012-01-01"

    def parse(self, response):
        """
        @url https://portaltransparencia.barramansa.rj.gov.br/boletim-oficial/
        @returns requests 1
        @returns items 15 15
        @scrapes date file_urls is_extra_edition power
        """
        for element in response.css("ul.ul-licitacoes li"):
            gazette_text = element.css("h4::text").get("")

            date_re = re.search(r"(\d{2} de (.*) de \d{4})", gazette_text)
            if not date_re:
                continue

            date_str = date_re.group(0)
            date_str = date_str.replace("Agosoto", "Agosto")
            date_str = date_str.replace("Dezembrbo", "Dezembro")
            
            parsed_date = dateparser.parse(date_str, languages=["pt"])
            if not parsed_date:
                continue
            date = parsed_date.date()

            path_to_gazette = element.css("a::attr(href)").get()
            if not path_to_gazette:
                continue
            path_to_gazette = path_to_gazette.strip()
            if path_to_gazette.startswith("up/diario_oficial.php"):
                path_to_gazette = response.urljoin(path_to_gazette)

            is_extra_edition = gazette_text.startswith("Suplemento")

            yield Gazette(
                date=date,
                file_urls=[path_to_gazette],
                is_extra_edition=is_extra_edition,
                power="executive",
            )

        next_url = response.xpath(
            "//a[contains(translate(text(), 'ÁÉÍÓÚ', 'AEIOU'), 'PROXIMA')]/@href"
        ).get()
        if next_url:
            yield Request(response.urljoin(next_url))
