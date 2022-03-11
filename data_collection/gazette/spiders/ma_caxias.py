from datetime import date

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

    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_DELAY": 2.0,
    }

    def start_requests(self):
        for date_of_interest in rrule(
            freq=DAILY, dtstart=self.start_date, until=self.end_date
        ):
            yield scrapy.FormRequest(
                url=self.BASE_URL,
                method="POST",
                formdata={
                    "date": date_of_interest.strftime(self.DATE_FORMAT),
                    "action": "_dom",
                },
                cb_kwargs={"gazette_date": date_of_interest.date()},
            )

    def parse(self, response, gazette_date):
        gazette_info = response.xpath("//div[@class='items']/p")
        if not gazette_info:
            self.logger.debug(f"No gazette for {gazette_date}")
            return

        for gazette in gazette_info:
            download_button = gazette.xpath(".//a[@class='btn-download']")
            url = download_button.xpath("@href")
            text = download_button.xpath("text()")

            gazette_error = gazette.xpath(
                "./preceding-sibling::div[1]/div[@class='gde-error']"
            )
            if gazette_error:
                self.logger.warning(
                    f"A document for {gazette_date} is not available: {url.get()}"
                )
                continue

            is_extra_edition = "extra" in url.get().lower() + text.get().lower()
            edition_number = (
                text.re_first(r"\d+") or url.re_first(r"\d{4}/\d{2}/(\d+)")
                if not is_extra_edition
                else ""
            )

            yield Gazette(
                date=gazette_date,
                file_urls=[url.get()],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power="executive",
            )
