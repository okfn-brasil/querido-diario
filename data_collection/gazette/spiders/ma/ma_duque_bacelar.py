import urllib.parse
from datetime import date
from typing import List

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaDuqueBacelar(BaseGazetteSpider):
    name = "ma_duque_bacelar"
    TERRITORY_ID = "2103901"
    allowed_domains = ["duquebacelar.ma.gov.br"]
    start_urls = ["https://duquebacelar.ma.gov.br/transparencia/diario-oficial"]
    start_date = date(2019, 8, 29)

    def _extract_url(self, url_element: scrapy.Selector):
        (raw_path,) = url_element.css("a")

        return urllib.parse.urljoin(
            "https://duquebacelar.ma.gov.br", raw_path.attrib.get("href")
        )

    def _extract_date(self, date_element: scrapy.Selector):
        day, month, year = date_element.xpath("text()").get().split("/")

        return date(int(year), int(month), int(day))

    def _extract_edition_number(self, edition_number_element: scrapy.Selector):
        return int(edition_number_element.xpath("text()").get())

    def _map_entries(self, gazette_element_list: List[scrapy.Selector]):
        output = []

        for gazette_element in gazette_element_list:
            (
                edition_number_element,
                _,
                __,
                date_element,
                ___,
                ____,
                url_element,
            ) = gazette_element.css("td")

            output.append(
                {
                    "edition_number": self._extract_edition_number(
                        edition_number_element
                    ),
                    "date": self._extract_date(date_element),
                    "url": self._extract_url(url_element),
                }
            )

        return sorted(output, key=lambda entry: entry.get("date"))

    def parse(self, response: scrapy.http.Response):
        _, *gazette_element_list, __ = response.css("tr")

        entries = [
            gazette_entry
            for gazette_entry in self._map_entries(gazette_element_list)
            if gazette_entry.get("date") >= self.start_date
            and gazette_entry.get("date") <= self.end_date
        ]

        for entry in entries:
            yield Gazette(
                edition_number=entry.get("edition_number"),
                date=entry.get("date"),
                file_urls=[entry.get("url")],
                power="executive",
            )
