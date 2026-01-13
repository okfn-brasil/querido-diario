import datetime as dt
import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMacaibaSpider(BaseGazetteSpider):
    name = "rn_macaiba"
    TERRITORY_ID = "2407104"
    allowed_domains = ["macaiba.rn.gov.br"]
    start_urls = ["https://macaiba.rn.gov.br/servicos/diario-oficial/"]
    start_date = dt.date(2013, 8, 9)

    def parse(self, response):
        follow_next_page = True

        for edition in response.css("li.link_item a"):
            url = edition.css("::attr(href)").get()
            raw_edition, raw_date = edition.css("::text").get().split(" - ")
            is_extra_edition = "xtra" in raw_edition
            edition_number = re.search(r"(\d+)", raw_edition).group(0).lstrip("0")
            date = dateparser.parse(raw_date).date()
    
            if date < self.start_date:
                follow_next_page = False
                break

            if date > self.end_date:
                continue

            yield Gazette(
                file_urls=[url],
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        if follow_next_page:
            next_page_url = response.css("a.nextpostslink::attr(href)").get()
            if next_page_url:
                yield scrapy.Request(next_page_url)
