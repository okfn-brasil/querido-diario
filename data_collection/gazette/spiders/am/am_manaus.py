import datetime
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AmManausSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True

    name = "am_manaus"
    allowed_domains = ["dom.manaus.am.gov.br"]
    start_date = datetime.date(2000, 4, 3)
    start_urls = ["http://dom.manaus.am.gov.br/diario-oficial-de-manaus"]

    TERRITORY_ID = "1302603"

    def parse(self, response):
        follow_next_page = True
        gazettes = response.css(".listing tbody tr")
        for gazette in gazettes:
            gazette_date_raw = gazette.xpath("./td[1]//text()").re_first(
                r"\d{2}\/\d{2}\/\d{4}"
            )
            gazette_date = datetime.datetime.strptime(
                gazette_date_raw, "%d/%m/%Y"
            ).date()

            if gazette_date < self.start_date:
                follow_next_page = False
                break

            title = "".join(gazette.xpath("./td[2]//text()").getall()).strip()
            edition_number = self._extract_edition_number(title, gazette_date)
            is_extra_edition = re.search(r"eex|ext", title.lower()) is not None
            gazette_url = gazette.css("a::attr(href)").get()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive",
            )

        if follow_next_page:
            next_page_url = response.css(".next a::attr(href)").get()
            yield scrapy.Request(next_page_url)

    def _extract_edition_number(self, text, gazette_date):
        year = gazette_date.year
        pattern = r"|".join(
            [
                r"Edição (\d+)\s",
                rf"dom{year}(\d{{4}})[A-Za-z.]",
                r"dom(\d{4})[A-Za-z.]",
                r"(\d+)\s",
            ]
        )
        matches = re.search(pattern, text)
        if matches:
            return matches.group(matches.lastindex)
        return ""
