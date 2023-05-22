import datetime as dt
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMossoroSpider(BaseGazetteSpider):
    TERRITORY_ID = "2408003"
    name = "rn_mossoro"
    start_date = dt.date(2023, 1, 1)
    allowed_domains = ["dom.mossoro.rn.gov.br"]
    start_urls = ["https://www.dom.mossoro.rn.gov.br/dom/edicoes"]

    def parse(self, response):
        for edition in response.css("div.edicoes-list div.col-md-3"):
            url = edition.css("a::attr(href)").get()
            raw_date = edition.css("div.card-content p::text").get().strip()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
            raw_edition_number = edition.css("div.card-content h4::text").get().strip()
            edition_number = re.findall(r"DOM N. (\d+)", raw_edition_number)

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=[f"https://www.dom.mossoro.rn.gov.br{url}"],
                is_extra_edition=False,
                power="executive_legislative",
            )

        next_page_url = response.xpath(
            "//a[contains(text(), 'PRÓXIMA PÁGINA')]/@href"
        ).get()
        if next_page_url:
            yield scrapy.Request(
                f"https://www.dom.mossoro.rn.gov.br{next_page_url}", callback=self.parse
            )
