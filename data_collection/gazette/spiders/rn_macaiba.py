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
    
    def start_requests(self):
        start_date_str = self.start_date.strftime("%Y-%m-%d")
        end_date_str = self.end_date.strftime("%Y-%m-%d")
        url = f"https://macaiba.rn.gov.br/?post_types=diario-oficial&post_date={start_date_str}+{end_date_str}"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for edition in response.css("li.link_item a"):
            url = edition.css("::attr(href)").get()
            raw_edition, raw_date = edition.css("::text").get().split(" - ")
            is_extra_edition = "xtra" in raw_edition
            edition_number = re.search(r"(\d+)", raw_edition).group(0).lstrip("0")
            date = dateparser.parse(raw_date).date()

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield Gazette(
                file_urls=[url],
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        next_page_url = response.css("a.nextpostslink::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(next_page_url, dont_filter=True)
