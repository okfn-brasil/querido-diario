from datetime import date, datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaCaxiasSpider(BaseGazetteSpider):

    name = "ma_caxias"
    allowed_domains = ["caxias.ma.gov.br"]
    start_date = date(2017, 3, 6)
    TERRITORY_ID = "2103000"
    BASE_URL = "https://caxias.ma.gov.br/diario-oficial-do-municipio"
    DATE_FORMAT = "%d/%m/%Y"

    def start_requests(self):
        for date_of_interest in rrule(
            freq=DAILY, dtstart=self.start_date, until=date.today()
        ):
            yield scrapy.FormRequest(
                url=self.BASE_URL,
                method="POST",
                formdata={
                    "date": date_of_interest.strftime(self.DATE_FORMAT),
                    "action": "_dom",
                },
            )

    def parse(self, response):
        gazette_info = response.xpath("//a[@class='btn-download']")
        gazette_error = response.xpath("//div[@class='gde-error']")

        if gazette_error or not gazette_info:
            return

        raw_date = response.xpath("//input[@id='date']/@value").get()
        gazette_date = datetime.strptime(raw_date, self.DATE_FORMAT)
        for gazette in gazette_info:
            url = gazette.xpath("@href")
            text = gazette.xpath("text()")

            is_extra_edition = "extra" in url.get().lower() + text.get().lower()
            edition_number = (
                text.re_first(r"\d+") or url.re_first(r"\d{4}/\d{2}/(\d+)")
                if not is_extra_edition
                else ""
            )

            yield Gazette(
                date=gazette_date.date(),
                file_urls=[url.get()],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power="executive",
            )
