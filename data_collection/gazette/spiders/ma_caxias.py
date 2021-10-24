from datetime import date, datetime

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaCaxiasSpider(BaseGazetteSpider):

    name = "ma_caxias"
    allowed_domains = ["caxias.ma.gov.br"]
    start_date = date(2017, 3, 6)
    url_base = "https://caxias.ma.gov.br/diario-oficial-do-municipio"
    TERRITORY_ID = "2103000"
    fmt_date = "%d/%m/%Y"

    def start_requests(self):
        days = rrule(freq=DAILY, dtstart=self.start_date, until=date.today())
        for day in days:
            yield scrapy.FormRequest(
                url=self.url_base,
                method="POST",
                formdata={"date": day.strftime(self.fmt_date), "action": "_dom"},
            )

    def parse(self, response):
        gazette_info = response.xpath("//a[@class='btn-download']")
        gazzete_error = response.xpath("//div[@class='gde-error']")
        if gazette_info and not (gazzete_error):
            day = response.xpath("//input[@id='date']/@value").get()
            gazette_date = datetime.strptime(day, self.fmt_date)
            for gazette in gazette_info:
                file_url = gazette.xpath("@href").get()
                is_extra_edition = "extra" in file_url.lower()
                edition_number = gazette.xpath("text()").re_first(r"\d+")

                yield Gazette(
                    date=gazette_date.date(),
                    file_urls=[file_url],
                    edition_number=edition_number,
                    is_extra_edition=is_extra_edition,
                    territory_id=self.TERRITORY_ID,
                    power="executive",
                    scraped_at=datetime.utcnow(),
                )
