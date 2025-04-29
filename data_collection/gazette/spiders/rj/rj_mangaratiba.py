import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjMangaratibaSpider(BaseGazetteSpider):
    name = "rj_mangaratiba"
    TERRITORY_ID = "3302601"
    allowed_domains = ["www.mangaratiba.rj.gov.br"]
    start_date = date(2012, 1, 1)

    def start_requests(self):
        years_range = range(self.start_date.year, self.end_date.year + 1)
        for year in years_range:
            yield scrapy.Request(
                f"https://www.mangaratiba.rj.gov.br/novoportal/publicacoes-ano.php?ano={year}"
            )

    def parse(self, response):
        for tr in response.css("tbody tr"):
            date_tmp = tr.css("td:nth-child(2)::text").get()
            date_tmp = dt.strptime(date_tmp, "%d/%m/%Y").date()

            if date_tmp > self.end_date:
                continue
            if date_tmp < self.start_date:
                return

            raw_edition = tr.css("td:nth-child(1)::text").get()
            match = re.search(r"^\d+", raw_edition)
            edition_number = match.group(0) if match else ""

            extra = not raw_edition.isdigit()

            gazzete_link = tr.css("td:nth-child(4) a::attr(onclick)").get()
            gazzete_link = gazzete_link.split("window.open('")[-1].split("','_blank'")[
                0
            ]

            yield Gazette(
                date=date_tmp,
                edition_number=edition_number,
                is_extra_edition=extra,
                file_urls=[gazzete_link],
                power="executive_legislative",
            )
