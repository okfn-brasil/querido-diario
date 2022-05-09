import datetime as dt
import re
from urllib.parse import unquote

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMossoroSpider(BaseGazetteSpider):
    name = "rn_mossoro"
    TERRITORY_ID = "2408003"
    allowed_domains = ["jom.prefeiturademossoro.com.br"]
    start_date = dt.date(2008, 1, 1)

    def start_requests(self):
        # avoid skipping months if day of start_date is at the end of the month
        first_day_of_start_date_month = dt.date(
            self.start_date.year, self.start_date.month, 1
        )
        months_of_interest = rrule(
            MONTHLY, dtstart=first_day_of_start_date_month, until=self.end_date
        )
        for month_date in months_of_interest:
            yield scrapy.Request(
                url=f"http://jom.prefeiturademossoro.com.br/{month_date.year}/{month_date.month}/"
            )

    def parse(self, response):
        for edition in response.css("article.post.category-jom"):
            url = edition.css("a:first-of-type::attr(href)").get()
            raw_date = edition.css("time.published::attr(datetime)").get()
            date = dt.datetime.fromisoformat(raw_date).date()

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield scrapy.Request(
                url,
                callback=self.parse_gazette,
                cb_kwargs={"date": date},
            )

        next_page_url = response.css("a.next::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(next_page_url)

    def parse_gazette(self, response, date):
        file_url = unquote(response.css("iframe::attr(src)").re_first(r"file=(.+)"))
        edition_regex = re.compile(r"JOM[n\s\.°º]+([a-z0-9]+)", re.IGNORECASE)
        edition_number = response.css(".entry-title::text").re_first(edition_regex)

        yield Gazette(
            date=date,
            edition_number=edition_number,
            file_urls=[file_url],
            is_extra_edition=False,
            power="executive_legislative",
        )
