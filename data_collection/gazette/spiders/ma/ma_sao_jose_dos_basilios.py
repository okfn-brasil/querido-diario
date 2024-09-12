import datetime

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaSaoJoseDosBasiliosSpider(BaseGazetteSpider):
    TERRITORY_ID = "2111250"
    name = "ma_sao_jose_dos_basilios"
    start_date = datetime.date(2015, 11, 27)
    allowed_domains = ["diariooficial.saojosedosbasilios.ma.gov.br"]
    BASE_URL = "https://diariooficial.saojosedosbasilios.ma.gov.br"

    def start_requests(self):
        yield scrapy.Request(f"{self.BASE_URL}/home")

    def parse(self, response, page=1):
        """
        Parse each page from the results page and yield the gazette issues available and go to next page.
        """
        gazette_boxes = response.css(
            "div#edicoes-anteriores.table-responsive table.table.table-bordered tbody tr"
        )

        for gazette_box in gazette_boxes:
            edition_number = (
                gazette_boxes.css("td:nth-child(1) a::text")
                .get()
                .strip()
                .split(" ")[3]
                .split("/")[0]
            )

            date = dateparser.parse(
                gazette_boxes.css("td:nth-child(3)::text").get().strip().split(",")[1],
                languages=["pt"],
            ).date()

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield Gazette(
                date=date,
                file_urls=[
                    f"{self.BASE_URL}/diariooficial/getFile/{edition_number}/download=true"
                ],
                edition_number=edition_number,
                power="executive_legislative",
            )

            next_page_url = response.css("a.page-link[rel='next']::attr(href)").get()
            if next_page_url:
                yield scrapy.Request(url=next_page_url)
