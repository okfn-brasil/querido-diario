import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpPauliniaSpider(BaseGazetteSpider):
    name = "sp_paulinia"
    TERRITORY_ID = "2905206"
    start_date = datetime.date(2012, 1, 4)
    allowed_domains = ["www.paulinia.sp.gov.br"]
    start_urls = ["http://www.paulinia.sp.gov.br/semanarios"]

    def parse(self, response):
        years = response.css("div.col-md-1")

        for year in years:
            year_to_scrape = int(year.xpath("./a/text()").get())

            if not (self.start_date.year <= year_to_scrape <= self.end_date.year):
                continue

            event_target = year.xpath("./a/@href").re_first(r"(ctl00.*?)',")

            yield scrapy.FormRequest.from_response(
                response,
                formdata={"__EVENTTARGET": event_target},
                callback=self.parse_year,
            )

        yield from self.parse_year(response)

    def parse_year(self, response):
        editions = response.css("div.body-content div.row a[href*='AbreSemanario']")

        for edition in editions:
            title = edition.xpath("./text()")
            gazette_date = datetime.datetime.strptime(
                title.re_first(r"\d{2}/\d{2}/\d{4}"),
                "%d/%m/%Y",
            ).date()

            if not (self.start_date <= gazette_date <= self.end_date):
                continue

            document_href = edition.xpath("./@href").get()
            edition_number = title.re_first(r"- (\d+) -")
            is_extra_edition = "extra" in title.get().lower()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[response.urljoin(document_href)],
                is_extra_edition=is_extra_edition,
                power="executive",
            )
