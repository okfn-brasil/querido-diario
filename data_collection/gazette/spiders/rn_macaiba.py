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
        for edition in response.xpath("//li[@class='link_item']"):
            url = edition.xpath(".//a/@href").get()
            raw_edition, raw_date = edition.xpath(".//a/text()").get().split(" - ")
            is_extra_edition = "xtra" in raw_edition
            edition_number = re.search(r"(\d+)", raw_edition).group(0)
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
                power="executive",
            )

        next_page_url = response.xpath("//a[@class='nextpostslink']/@href").get()
        if next_page_url:
            yield scrapy.Request(next_page_url)
