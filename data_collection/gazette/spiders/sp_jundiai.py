import datetime as dt

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpJundiaiSpider(BaseGazetteSpider):
    TERRITORY_ID = "3525904"
    name = "sp_jundiai"
    allowed_domains = ["jundiai.sp.gov.br"]
    start_date = dt.date(2006, 4, 4)

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
                url=f"https://imprensaoficial.jundiai.sp.gov.br/{month_date.year}/{month_date.month}/"
            )

    def parse(self, response, current_page=1):
        editions = response.css("#lista-edicoes li.edicao-atual")
        for edition in editions:
            raw_date = edition.xpath("./a/span[2]/text()").get()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            gazette_url = edition.css("a::attr(href)").extract_first()
            if gazette_url:
                yield scrapy.Request(
                    gazette_url, callback=self.parse_gazette, cb_kwargs={"date": date}
                )

        pagination = response.css("div.paginacao > span.page::text")
        if not pagination:
            return

        number_of_pages = int(pagination.re_first(r"de\s+(\d+)"))
        if current_page < number_of_pages:
            yield scrapy.Request(
                f"{response.url}/page/{current_page + 1}",
                callback=self.parse,
                cb_kwargs={"current_page": current_page + 1},
            )

    def parse_gazette(self, response, date):
        file_urls = response.css("div.edicao-download a::attr(href)").getall()
        title = response.css("div.edicao-titulo::text")
        is_extra_edition = "extra" in title.get().lower()
        edition_number = title.re_first(r"\d+")

        yield Gazette(
            date=date,
            file_urls=file_urls,
            edition_number=edition_number,
            is_extra_edition=is_extra_edition,
            power="executive_legislative",
        )
