import datetime
import re

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AlMaceioSpider(BaseGazetteSpider):
    TERRITORY_ID = "2704302"

    name = "al_maceio"
    allowed_domains = ["maceio.al.gov.br"]
    start_date = datetime.date(2013, 1, 10)

    def start_requests(self):
        initial_date = self.start_date
        end_date = datetime.date.today()

        current_date = initial_date
        while current_date <= end_date:
            url = f"http://www.maceio.al.gov.br/{current_date.year}/{current_date.month}/{current_date.day}/?post_type=downloads&cat=13003"
            yield scrapy.Request(url)
            current_date = current_date + datetime.timedelta(days=1)

    def parse(self, response):
        gazettes = response.xpath("//article")
        for gazette in gazettes:
            gazette_date = gazette.xpath("time/text()").get()
            gazette_date = parse(gazette_date, languages=["pt"]).date()

            title = gazette.xpath("a/@title").get()
            is_extra_edition = bool(
                re.search(r"suplemento|suplementar|extraordinária", title.lower())
            )

            download_url = gazette.xpath("a/@href").get()

            if "wp-content/uploads" in download_url:
                yield self.create_gazette(gazette_date, download_url, is_extra_edition)
            else:
                yield scrapy.Request(
                    download_url,
                    callback=self.parse_additional_page,
                    meta={
                        "gazette_date": gazette_date,
                        "is_extra_edition": is_extra_edition,
                    },
                )

    def parse_additional_page(self, response):
        url = response.css("p.attachment a::attr(href)").get()
        yield self.create_gazette(
            response.meta["gazette_date"], url, response.meta["is_extra_edition"]
        )

    def create_gazette(self, date, url, is_extra_edition):
        return Gazette(
            date=date,
            file_urls=[url],
            is_extra_edition=is_extra_edition,
            power="executive",
        )
