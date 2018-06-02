import re
import json
import itertools
import dateparser

from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class DfBrasiliaSpider(BaseGazetteSpider):
    TERRITORY_ID = "5300108"
    GAZETTE_URL = "http://dodf.df.gov.br/listar"

    MONTHS = {
        "12": "12_Dezembro",
        "11": "11_Novembro",
        "10": "10_Outubro",
        "09": "09_Setembro",
        "08": "08_Agosto",
        "07": "07_Julho",
        "06": "06_Junho",
        "05": "05_Maio",
        "04": "04_Abril",
        "03": "03_Março",
        "02": "02_Fevereiro",
        "01": "01_Janeiro",
    }
    YEARS = ["2018", "2017", "2016", "2015"]
    MONTHS_YEARS = itertools.product(MONTHS.values(), YEARS)

    DATE_REGEX = r"DODF [0-9]+ ([0-9]{2}-[0-9]{2}-[0-9]{4})(.*)$"
    EXTRA_EDITION_TEXT = "EDICAO EXTR"
    PDF_URL = "http://dodf.df.gov.br/index/visualizar-arquivo/?pasta={}&arquivo={}"

    allowed_domains = ["dodf.df.gov.br"]
    name = "df_brasilia"

    def start_requests(self):
        for month, year in self.MONTHS_YEARS:
            yield Request(f"{self.GAZETTE_URL}?dir={year}/{month}", self.parse_month)

    def parse_month(self, response):
        json_response = json.loads(response.body_as_unicode())
        dates = json_response["data"]

        if not dates:
            return

        for gazette_name in dates.values():
            date = re.search(self.DATE_REGEX, gazette_name).group(1)
            day, month, year = date.split("-")
            url = f"{self.GAZETTE_URL}?dir={year}/{self.MONTHS[month]}/{gazette_name}"
            yield Request(url)

    def parse(self, response):
        """
        @url http://dodf.df.gov.br/listar?dir=2018/05_Maio/DODF%20097%2022-05-2018%20SUPLEMENTO
        @returns items 1
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """

        json_response = json.loads(response.body_as_unicode())

        if not json_response:
            return

        json_dir = json_response["dir"]
        json_data = json_response["data"]

        date = dateparser.parse(json_dir)
        is_extra_edition = self.EXTRA_EDITION_TEXT in json_dir

        path = json_dir.replace("/", "|")
        file_urls = [self.PDF_URL.format(path, url.split("/")[-1]) for url in json_data]

        yield Gazette(
            date=date,
            file_urls=file_urls,
            is_extra_edition=is_extra_edition,
            territory_id=self.TERRITORY_ID,
            scraped_at=datetime.utcnow(),
            power="executive_legislative",
        )
