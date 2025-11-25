import json
import re
from datetime import date, datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpOsascoSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "3534401"
    name = "sp_osasco"
    allowed_domains = ["www.osasco.sp.gov.br"]
    start_urls = ["https://www.osasco.sp.gov.br/imprensa-oficial/"]
    start_date = date(2002, 8, 2)
    NUMBER_REGEX = re.compile(r"(\d+)$")

    def parse(self, response):
        gazettes = json.loads(
            response.xpath('//script[contains(text(), "DOCS")]/text()').re_first(
                "var DOCS = (.*);"
            )
        )

        for gazette in gazettes:
            edition_date = datetime.strptime(gazette["date"], "%d / %m / %Y").date()

            if not self.start_date <= edition_date <= self.end_date:
                continue

            edition_number = None
            if edition_number_m := self.NUMBER_REGEX.search(gazette["title"]):
                edition_number = edition_number_m.group()

            url = gazette["url"]
            if not url:
                self.logger.warning(f"Unable to find download URL for: {gazette}.")
                continue

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                file_urls=[url],
                is_extra_edition=False,
                power="executive",
            )
