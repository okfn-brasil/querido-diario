import re
from datetime import date, datetime
from urllib.parse import quote

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjMacucoSpider(BaseGazetteSpider):
    name = "rj_macuco"
    TERRITORY_ID = "3302452"
    allowed_domains = ["prefeituramacuco.rj.gov.br"]
    start_date = date(2021, 3, 5)

    def start_requests(self):
        start_year = self.start_date.year
        end_year = self.end_date.year
        for year in range(start_year, end_year + 1):
            url = f"https://prefeituramacuco.rj.gov.br/transparencia_api/diario/buscar?ano={year}"
            yield scrapy.Request(url)

    def parse(self, response):
        data = response.json()
        for gazette in data:
            date_str = gazette.get("data_p")
            date_str = date_str[:10]
            file_url = "https://prefeituramacuco.rj.gov.br/transparencia" + quote(
                gazette.get("arquivo")
            )
            edition_number = gazette.get("edicao", "")
            edition_number = re.sub(r"\D", "", edition_number)
            is_extra_edition = "suplementar" in gazette.get("arquivo", "").lower()

            publication_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            if publication_date > self.end_date:
                continue

            if publication_date < self.start_date:
                return

            yield Gazette(
                date=publication_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[file_url],
                power="executive",
            )
