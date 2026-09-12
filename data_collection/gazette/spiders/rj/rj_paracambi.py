import re
from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjParacambiSpider(BaseGazetteSpider):
    name = "rj_paracambi"
    TERRITORY_ID = "3303609"
    allowed_domains = ["paracambi.rj.gov.br"]
    start_urls = ["https://paracambi.rj.gov.br/diario-oficial-eletronico-2025/"]
    start_date = date(2020, 2, 4)

    def parse(self, response):
        years_link = response.css(
            "a.wp-block-button__link.has-background.wp-element-button::attr(href)"
        ).getall()
        for link in years_link:
            year = int(re.sub(r"\D", "", link))
            if self.start_date.year <= year <= self.end_date.year:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_month,
                    cb_kwargs={"year": year},
                )

    def parse_month(self, response, year):
        months = response.css("div.tab-content div.tab-pane")
        for month in months:
            current_month = month.css("::attr(id)").get()
            current_month = int(re.search(r"(\d+)$", current_month).group()) + 1

            current_date = date(year, current_month, 1)

            if current_date < date(self.start_date.year, self.start_date.month, 1):
                continue

            if current_date > date(self.end_date.year, self.end_date.month, 1):
                return

            days = month.css("li")
            for day in days:
                edition_text = day.css("a::text").get() or day.css("span::text").get()
                if not edition_text:
                    continue

                date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", edition_text)
                if not date_match:
                    continue

                edition_date = datetime.strptime(date_match.group(), "%d.%m.%Y").date()

                if not self.start_date <= edition_date <= self.end_date:
                    continue

                edition_url = day.css("a::attr(href)").get()
                extra_edition = "extra" in edition_text.lower()

                edition_num_match = re.search(r"Ed(\d+)", edition_text)
                edition_num = edition_num_match.group(1) if edition_num_match else None

                yield Gazette(
                    date=edition_date,
                    edition_number=edition_num,
                    is_extra_edition=extra_edition,
                    file_urls=[edition_url],
                    power="executive",
                )
