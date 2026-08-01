import re
from datetime import datetime
from urllib.parse import urlparse

import scrapy
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class BaseImprensaOficialSpider(BaseGazetteSpider):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, "url_base"):
            raise NotConfigured("Please set a value for `url_base`")

        domains = {
            "imprensaoficial.org",
            urlparse(self.url_base).netloc,
        }
        self.allowed_domains = list(domains)

        super(BaseImprensaOficialSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for year_month in monthly_sequence(
            self.start_date, self.end_date, format="%Y/%m/"
        ):
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
