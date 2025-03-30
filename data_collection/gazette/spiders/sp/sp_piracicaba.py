import datetime
import urllib.parse

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import daily_sequence


class SpPiracicabaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3538709"
    name = "sp_piracicaba"
    allowed_domains = ["diariooficial.piracicaba.sp.gov.br"]

    start_date = datetime.date(2009, 3, 1)

    def start_requests(self):
        for date in daily_sequence(self.start_date, self.end_date, format="%Y/%m/%d"):
            yield scrapy.Request(f"https://diariooficial.piracicaba.sp.gov.br/{date}/")

    def parse(self, response):
        iframe = response.css("iframe")
        if not iframe:
            # If iframe is not present on page, we don't have a valid gazette
            # in the response
            return

        parts_script = response.xpath("//script[contains(., 'pdfjs-frame')]")
        if parts_script:
            file_urls = parts_script.re(r"\(\'src\', \'(.*)\'\);")
        else:
            query_src = urllib.parse.urlparse(iframe.css("::attr(src)").get()).query
            file_urls = urllib.parse.parse_qs(query_src).get("file", [])

        gazette_year = response.css(
            "#diario-select-year option[selected]::attr(value)"
        ).get()
        gazette_month = response.css(
            "#diario-select-month option[selected]::attr(value)"
        ).get()
        gazette_day = response.css(
            "#diario-select-day option[selected]::attr(value)"
        ).get()
        gazette_date = datetime.date(
            int(gazette_year), int(gazette_month), int(gazette_day)
        )

        yield Gazette(
            date=gazette_date,
            file_urls=file_urls,
            is_extra_edition=False,
            power="executive_legislative",
        )
