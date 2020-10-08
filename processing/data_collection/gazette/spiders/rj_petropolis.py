import os
import re
from datetime import datetime
from urllib.parse import urljoin

import scrapy
import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjPetropolis(BaseGazetteSpider):
    TERRITORY_ID = "3303906"
    BASE_URL = "http://www.petropolis.rj.gov.br"

    name = "rj_petropolis"
    allowed_domains = ["petropolis.rj.gov.br"]
    start_urls = [
        "http://www.petropolis.rj.gov.br/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/3-diario-oficial.html"
    ]
    set_to_discard = {
        "/pmp/index.php/servicos-na-web/informacoes/diario-oficial.html",
        None,
    }

    def parse(self, response):
        for entry in response.css("#col1 > div > table"):
            entry_url = entry.css("a::attr(href)").get()
            if entry_url not in self.set_to_discard:
                url = urljoin(self.BASE_URL, entry_url)
                if re.search(r"\d+-\d+", url):
                    yield scrapy.Request(url=url, callback=self.parse)
                else:
                    yield scrapy.Request(url=url, callback=self.parse_items_page)

    def parse_items_page(self, response):
        for entry in response.css("#col1 > div > table"):
            entry_url = entry.css("a::attr(href)").get()
            if entry_url not in self.set_to_discard:
                url = urljoin(self.BASE_URL, entry_url)
                file_url = url.replace(".html", ".pdf")

                date_match = re.search(r"(\d+-de-\w+-de-\d+)|(\d+-\d+-\d+)", url)
                is_extra_edition = "suplemento" in url
                edition_number = re.search(r"\d+-(\d+)", url).group(1)

                if date_match is not None:
                    date = dateparser.parse(
                        date_match.group(0), languages=["pt"]
                    ).date()

                    yield Gazette(
                        date=date,
                        file_urls=[file_url],
                        is_extra_edition=is_extra_edition,
                        territory_id=self.TERRITORY_ID,
                        power="executive_legislative",
                        scraped_at=datetime.utcnow(),
                        edition_number=edition_number,
                    )
