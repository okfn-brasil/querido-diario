from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RrPacaraimaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1400456"
    name = "rr_pacaraima"
    allowed_domains = ["pacaraima.rr.gov.br"]
    base_url = "http://www.pacaraima.rr.gov.br/diario-oficial"
    start_date = date(2017, 1, 2)

    def get_url(self, year):
        return f"{self.base_url}/{year}"

    def start_requests(self):
        yield Request(self.get_url(self.end_date.year))

    def parse(self, response):
        gazettes = response.css(".table tbody tr")
        for gazette in gazettes:
            raw_gazette_date = gazette.css("td::text").re_first(r"\d{2}\/\d{2}\/\d{4}")
            gazette_date = datetime.strptime(raw_gazette_date, "%d/%m/%Y").date()

            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            gazette_url = gazette.css("a::attr(href)").get()
            if gazette_url is None:
                self.logger.warn(f"Unable to retrieve PDF URL for {gazette_date}.")
                continue

            edition_number = gazette.css("td::text").re_first(r"DO.*")
            is_extra_edition = gazette.css("td::text").re_first(r"EXTRA*") is not None

            item = Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive",
            )

            yield Request(
                gazette_url, callback=self.parse_gazette_url, cb_kwargs={"item": item}
            )

        year_to_scrap = gazette_date.year - 1
        if year_to_scrap >= self.start_date.year:
            yield Request(self.get_url(year_to_scrap), callback=self.parse)

    def parse_gazette_url(self, response, item):
        gazette_url = response.css("a::attr(href)").get()
        yield Gazette(
            file_urls=[
                gazette_url,
            ],
            **item,
        )
