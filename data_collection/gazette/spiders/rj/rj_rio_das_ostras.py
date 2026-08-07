import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjRioDasOstrasSpider(BaseGazetteSpider):
    name = "rj_rio_das_ostras"
    TERRITORY_ID = "3304524"
    allowed_domains = ["riodasostras.rj.gov.br"]
    start_date = date(2001, 7, 13)

    def start_requests(self):
        for year in range(self.start_date.year, self.end_date.year + 1):
            base_url = f"https://appro.riodasostras.rj.gov.br/riodasostrasapp_server/api/jornais/search/site?&limit=600&offset=0&orderBy=data&orderDir=desc&ano={year}"
            yield scrapy.Request(base_url)

    def parse(self, response):
        for gazette_data in response.json():
            raw_gazette_date = gazette_data["data"][:10]
            gazette_date = dt.strptime(raw_gazette_date, "%Y-%m-%d").date()

            if gazette_date > self.end_date:
                continue

            if gazette_date < self.start_date:
                return

            match = re.search(r"Edição.*?(\d+)", gazette_data["edicao"])
            gazette_edition_number = "" if match is None else match.group(1)
            is_extra_edition = bool(
                re.search(
                    r"anex|encar|loa|ppa|ldo|conc",
                    gazette_data["edicao"],
                    re.IGNORECASE,
                )
            )
            gazette_url = gazette_data["link"]

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive_legislative",
            )
