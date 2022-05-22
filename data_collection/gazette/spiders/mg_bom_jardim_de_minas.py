import re

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class barramansaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3107505"

    allowed_domains = ["https://www.bomjardimdeminas.mg.gov.br"]
    name = "mg_bom_jardim_de_minas"
    start_urls = [
        "https://www.bomjardimdeminas.mg.gov.br/diariobj/"
    ]

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

            date = date_re.group(0)
            # The extra edition for August 28th, 2018 has a typo in the month name.
            date = date.replace("Agosoto", "Agosto")
            # The edition for December 17th, 2012 has a typo in the month name.
            date = date.replace("Dezembrbo", "Dezembro")
            date = dateparser.parse(date, languages=["pt"]).date()

            path_to_gazette = element.css("a::attr(href)").get().strip()
            # From November 17th, 2017 and backwards the path to the gazette PDF
            # is relative.
            if path_to_gazette.startswith("up/diario_oficial.php"):
                path_to_gazette = response.urljoin(path_to_gazette)

            is_extra_edition = gazette_text.startswith("Suplemento")

            yield Gazette(
                date=date,
                file_urls=[path_to_gazette],
                is_extra_edition=is_extra_edition,
                power="executive",
            )

        next_url = (
            response.css(".pagination")
            .xpath("//a[contains(text(), 'Proxima')]/@href")
            .get()
        )
        if next_url:
            yield Request(response.urljoin(next_url))
