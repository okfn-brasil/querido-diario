import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjMacaeSpider(BaseGazetteSpider):
    TERRITORY_ID = "3302403"
    name = "rj_macae"
    allowed_domains = ["macae.rj.gov.br"]
    start_date = date(2020, 5, 22)

    def start_requests(self):
        yield scrapy.FormRequest(
            url="https://sistemas.macae.rj.gov.br:840/diariooficial/index/listarajax",
            method="POST",
            formdata={
                "periodode": self.start_date.strftime("%d/%m/%Y"),
                "periodoate": self.end_date.strftime("%d/%m/%Y"),
            },
        )

    def parse(self, response):
        for data in response.json()["data"]:
            gazette_code = data["DT_RowId"]
            gazette_url = f"https://sistemas.macae.rj.gov.br:840/diariooficial/index/download?id={gazette_code}"

            gazette_edition = data["edicao"]
            gazette_edition_number = re.search(r"\d+", gazette_edition).group(0)

            raw_gazette_date = data["publicacao"][0:10]
            gazette_date = dt.strptime(raw_gazette_date, "%d/%m/%Y").date()

            gazette_item = {
                "date": gazette_date,
                "edition_number": gazette_edition_number,
                "is_extra_edition": "EXTRA" in gazette_edition.upper(),
            }

            yield scrapy.Request(
                url=gazette_url,
                method="HEAD",
                callback=self.parse_pdf_url,
                cb_kwargs={"gazette_item": gazette_item},
            )

    def parse_pdf_url(self, response, gazette_item):
        yield Gazette(
            **gazette_item, file_urls=[response.url], power="executive_legislative"
        )
