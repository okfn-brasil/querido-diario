import datetime

import dateparser
import scrapy
import w3lib
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgUberlandiaSpider(BaseGazetteSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "3170206"
    name = "mg_uberlandia"
    start_date = datetime.date(2005, 1, 3)

    def start_requests(self):
        first_day_of_start_date_month = datetime.date(
            self.start_date.year, self.start_date.month, 1
        )
        months_of_interest = rrule(
            MONTHLY, dtstart=first_day_of_start_date_month, until=self.end_date
        )
        for month_date in months_of_interest:
            yield scrapy.Request(
                f"https://www.uberlandia.mg.gov.br/{month_date.year}/{month_date.month}/?post_type=diariooficial",
                errback=self.on_error,
            )

    def on_error(self, failure):
        # month/year URLs have two different valid query parameters:
        # post_type=diario_oficial or post_type=diariooficial
        # so if the first is not found, it will retry with the second type
        if failure.value.response.status == 404:
            alternative_url = w3lib.url.add_or_replace_parameter(
                failure.value.response.url, "post_type", "diario_oficial"
            )
            yield scrapy.Request(alternative_url)

    def parse(self, response):
        gazettes = response.css("article.elementor-post")
        for gazette in gazettes:
            gazette_date = dateparser.parse(
                gazette.css(
                    ".elementor-post-date::text, .ee-post__metas__date::text"
                ).get()
            ).date()
            if gazette_date < self.start_date or gazette_date > self.end_date:
                continue

            edition = gazette.css("h3 a::text, h5::text")
            edition_number = edition.re_first(r"(\d+)")
            is_extra_edition = bool(edition.re(r"\d+.*?([A-Za-z]+)"))

            gazette_url = gazette.css("a::attr(href)").get()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive",
            )

        for page_url in response.css("nav a.page-numbers::attr(href)").getall():
            yield scrapy.Request(page_url)
