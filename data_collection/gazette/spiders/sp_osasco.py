import json
import re
from datetime import datetime,date

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpOsascoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3534401"
    name = "sp_osasco"
    allowed_domains = ["www.osasco.sp.gov.br"]
    start_urls = ["http://www.osasco.sp.gov.br/imprensa-oficial/"]
    start_date = date(2002, 8, 2)

    NUMBER_REGEX = re.compile(r"\s(\d+)$")

    def parse(self, response):
        gazettes = json.loads(
            response.xpath('//script[contains(text(), "DOCS")]/text()').re_first(
                "var DOCS = (.*);"
            )
        )

        for gazette in gazettes:
            edition_date = dateparser.parse(
                gazette["date"], settings={"DATE_ORDER": "DMY"}
            )
            edition_date = edition_date.date()

            if not (self.start_date <= edition_date <= self.end_date):
                continue

            number = None
            match = self.NUMBER_REGEX.search(gazette["title"])
            if match:
                number = match.group(1)

            url = gazette["url"]

            yield Gazette(
                date=edition_date,
                edition_number=number,
                file_urls=[url],
                is_extra_edition=False,
                scraped_at=datetime.utcnow(),
                power="executive",
            )
