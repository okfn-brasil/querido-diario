import urllib.parse
from datetime import date

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaDuqueBacelar(BaseGazetteSpider):
    name = "ma_duque_bacelar"
    TERRITORY_ID = "2103901"
    allowed_domains = ["duquebacelar.ma.gov.br"]
    start_urls = ["https://duquebacelar.ma.gov.br/transparencia/diario-oficial"]
    start_date = date(2019, 8, 29)

    def _extract_url(self, element):
        return urllib.parse.urljoin(
            "https://duquebacelar.ma.gov.br", element.css("a").attrib.get("href")
        )

    def _extract_date(self, element):
        day, month, year = element.xpath("text()").get().split("/")

        return date(int(year), int(month), int(day))

    def _extract_edition_number(self, element):
        return int(element.xpath("text()").get())

    def parse(self, response):
        for gazette_row in response.css("tr")[1:-2]:
            gazette_cell_list = gazette_row.css("td")

            date = self._extract_date(gazette_cell_list.css("[data-order]"))

            if date >= self.start_date and date <= self.end_date:
                yield Gazette(
                    edition_number=self._extract_edition_number(
                        gazette_cell_list.pop(0)
                    ),
                    date=date,
                    file_urls=[self._extract_url(gazette_cell_list.pop())],
                    power="executive",
                )
