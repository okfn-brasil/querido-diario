import datetime as dt
import re

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMossoroSpider(BaseGazetteSpider):
    TERRITORY_ID = "2408003"
    name = "rn_mossoro"
    allowed_domains = ["jom.mossoro.rn.gov.br", "dom.mossoro.rn.gov.br"]
    start_date = dt.date(2008, 1, 1)

    TRANSITION_DATE = dt.date(2023, 1, 1)
    NEW_WEBSITE = "https://www.dom.mossoro.rn.gov.br"

    def start_requests(self):
        # use old website for dates before the transition date
        if self.start_date < self.TRANSITION_DATE:
            # avoid skipping months if day of start_date is at the end of the month
            first_day_of_start_date_month = dt.date(
                self.start_date.year, self.start_date.month, 1
            )
            months_of_interest = rrule(
                MONTHLY,
                dtstart=first_day_of_start_date_month,
                until=self.end_date
                if self.end_date < self.TRANSITION_DATE
                else self.TRANSITION_DATE - dt.timedelta(days=1),
            )
            for month_date in months_of_interest:
                yield scrapy.Request(
                    url=f"http://jom.mossoro.rn.gov.br/{month_date.year}/{month_date.month}/"
                )

        # use new website for dates after the transition date
        if self.end_date >= self.TRANSITION_DATE:
            yield scrapy.Request(
                url=f"{self.NEW_WEBSITE}/dom/edicoes",
                callback=self.parse_new_website,
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

    def parse_new_website(self, response):
        for edition in response.css("div.edicoes-list div.col-md-3"):
            url = edition.css("a::attr(href)").get()
            raw_date = edition.css("div.card-content p::text").get().strip()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
            edition_number = edition.css("div.card-content h4::text").get().strip()

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield scrapy.Request(
                f"{self.NEW_WEBSITE}{url}",
                callback=self.parse_gazette,
                cb_kwargs={"date": date, "edition_number": edition_number},
            )

        next_page_url = response.xpath(
            "//a[contains(text(), 'PRÓXIMA PÁGINA')]/@href"
        ).get()
        if next_page_url:
            yield scrapy.Request(
                f"{self.NEW_WEBSITE}{next_page_url}", callback=self.parse_new_website
            )

    def parse_gazette(self, response, date, edition_number=None):
        # parse gazette from old website
        if not edition_number:
            file_url = response.xpath("//a[contains(text(), 'Baixar')]/@href").get()
            edition_regex = re.compile(r"JOM[n\s\.°º]+([a-z0-9]+)", re.IGNORECASE)
            edition_number = response.css(".entry-title::text").re_first(edition_regex)
        else:
            file_url = response.xpath("//a[contains(text(), 'Download')]/@href").get()
            file_url = f"{self.NEW_WEBSITE}{file_url}"

        yield Gazette(
            date=date,
            edition_number=edition_number,
            file_urls=[file_url],
            is_extra_edition=False,
            power="executive_legislative",
        )
