import re
from datetime import date, datetime

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ImprensaOficialSpider(BaseGazetteSpider):
    def start_requests(self):
        initial_date = date(self.start_date.year, self.start_date.month, 1)

        for monthly_date in rrule(
            freq=MONTHLY, dtstart=initial_date, until=self.end_date
        ):
            year_month = monthly_date.strftime("%Y/%m/")  # like 2015/01
            yield scrapy.Request(
                self.url_base.format(year_month), callback=self.extract_gazette_links
            )

    def extract_gazette_links(self, response):
        for gazette_link in response.css("h2 a::attr(href)").getall():
            raw_gazette_date = re.search(r"\d{4}/\d{2}/\d{2}", gazette_link).group()
            gazette_date = datetime.strptime(raw_gazette_date, "%Y/%m/%d").date()
            if gazette_date < self.start_date:
                return
            yield scrapy.Request(gazette_link)

        # pagination exists when the button "Publicações mais antigas" is in the page
        another_page = response.xpath(
            ".//a[contains(text(), 'Publicações mais antigas')]/@href"
        ).get()
        if another_page:
            yield scrapy.Request(another_page, callback=self.extract_gazette_links)

    def parse(self, response):
        file_url = response.css(
            "div.entry-content a[href*='baixar.php?arquivo=']::attr(href)"
        ).get()
        if not file_url:  # older dates
            file_url = response.css(
                "div.entry-content a[title='Baixar Diário']::attr(href)"
            ).get()
        gazette_date = response.css("span.posted-on a time::attr(datetime)").get()
        gazette_date = datetime.strptime(gazette_date, "%Y-%m-%dT%H:%M:%S%z").date()

        yield Gazette(
            date=gazette_date,
            file_urls=[file_url],
            is_extra_edition=False,
            power="executive",
        )
