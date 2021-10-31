import json
import re
from datetime import date

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpOsascoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3534401"
    name = "sp_osasco"
    allowed_domains = ["www.osasco.sp.gov.br"]
    start_urls = ["http://www.osasco.sp.gov.br/imprensa-oficial/"]
    start_date = date(2002, 8, 2)

    ONLY_JSON_REGEX = re.compile("(\\[.*}]);")
    NUMBER_REGEX = re.compile("\\s([0-9]+)$")

    def parse(self, response):
        documents_json = response.xpath(
            '//script[contains(text(), "DOCS")]'
        ).extract_first()
        match = self.ONLY_JSON_REGEX.search(documents_json)

        if not match:
            raise "Gazette metadata not found"

        documents_json = match.group(1)
        gazettes = json.loads(documents_json)

        for gazette in gazettes:
            edition_date = dateparser.parse(
                gazette["date"], settings={"DATE_ORDER": "DMY"}
            )
            edition_date = edition_date.date()

            if edition_date < self.start_date:
                continue
            if edition_date > self.end_date:
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
                power="executive",
            )
