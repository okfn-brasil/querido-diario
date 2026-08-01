import datetime as dt
import re
from urllib.parse import urlparse, urlunparse

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import yearly_sequence


class BaBarreirasSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True

    name = "ba_barreiras"
    TERRITORY_ID = "2903201"
    allowed_domains = ["barreiras.ba.gov.br"]
    base_url = "https://barreiras.ba.gov.br/diario-oficial"
    start_date = dt.date(2008, 1, 2)

    def start_requests(self):
        for year in yearly_sequence(self.start_date, self.end_date):
            if year == dt.date.today().year:
                base_url = f"{self.base_url}/"
            else:
                base_url = f"{self.base_url}-{year}/"

            yield scrapy.Request(url=base_url)

    def parse(self, response):
        editions = response.css("div.content .style16")

        for edition in editions:
            link = edition.xpath(".//@href").get()
            metadata_str = "".join(edition.xpath(".//text()").getall())
            raw_date = re.search(r"\d{2}/\d{2}/\d{4}", metadata_str).group()
            gazette_date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
            gazette_edition = re.search(r"Edição (\d+)", metadata_str)

            edition_number = ""
            if gazette_edition is not None:
                edition_number = gazette_edition.group(1)

            is_extra_edition = False
            if "extra" in metadata_str.lower():
                is_extra_edition = True

            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            yield Gazette(
                power="executive",
                file_urls=[self._url_fix(link)],
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
            )

    def _url_fix(self, link):
        link = urlparse(link)
        link = link._replace(scheme="https")
        return urlunparse(link)
