import datetime
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

RE_EDITION_NUMBER = re.compile(r"Edi..o\s*(\d+)")
RE_EXT_DATE = re.compile(r"\s+(\d+)\sde\s(\w+)\sde\s(\d+)")


class PaCameta(BaseGazetteSpider):
    TERRITORY_ID = "1502103"
    name = "pa_cameta"
    allowed_domains = ["prefeituradecameta.pa.gov.br"]
    start_date = datetime.date(2023, 1, 12)

    BASE_URL = "https://prefeituradecameta.pa.gov.br/diario-oficial-do-municipio/"

    def start_requests(self):
        url = f"{self.BASE_URL}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        a_elements = response.css("#post-20884 > div > ul > li > a")
        for a in a_elements:
            text = a.css("a::text").get()
            href = a.css("a::attr(href)").get()
            # This link seems to be a test. will be ignored
            if "12 de abril de 2022" in text:
                continue
            gazette_edition_number = PaCameta.get_edition_number(text)
            gazette_date = PaCameta.get_date(text)
            gazette_url = href
            if self.start_date <= gazette_date <= self.end_date:
                yield Gazette(
                    date=gazette_date,
                    edition_number=gazette_edition_number,
                    file_urls=[gazette_url],
                    is_extra_edition=False,
                    power="executive",
                )

    @staticmethod
    def get_edition_number(text):
        match = RE_EDITION_NUMBER.search(text)
        return PaCameta.get_group(match)

    @staticmethod
    def get_group(match, number=1):
        return str(match.group(number)) if match else ""

    @staticmethod
    def get_date(text):
        months_pt_br = {
            "janeiro": 1,
            "fevereiro": 2,
            "março": 3,
            "abril": 4,
            "maio": 5,
            "junho": 6,
            "julho": 7,
            "agosto": 8,
            "setembro": 9,
            "outubro": 10,
            "novembro": 11,
            "dezembro": 12,
        }

        match = RE_EXT_DATE.search(text)

        first_group = PaCameta.get_group(match, 1)
        second_group = PaCameta.get_group(match, 2)
        third_group = PaCameta.get_group(match, 3)

        day = int(first_group)
        month = months_pt_br[second_group.lower()]
        year = int(third_group.zfill(4))
        return datetime.date(year, month, day)
