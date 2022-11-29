import datetime

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ApMacapaSpider(BaseGazetteSpider):
    name = "ap_macapa"
    allowed_domains = ["macapa.ap.gov.br"]
    start_date = datetime.date(2018, 1, 1)
    TERRITORY_ID = "1600303"

    def start_requests(self):
        base_url = "http://macapa.ap.gov.br/page/1/"
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")
        params = {
            "s": "",
            "post_type": "official_diaries",
            "search": "official_diaries",
            "official_diary_initial_date": start_date,
            "official_diary_final_date": end_date,
        }
        yield scrapy.FormRequest(
            url=base_url,
            method="GET",
            formdata=params,
            callback=self._pagination_requests,
            cb_kwargs={"params": params},
        )

    def _pagination_requests(self, response, params):
        pages = response.xpath("//a[@class='page-numbers']/text()").getall()
        if pages:
            last_page = max([int(page) for page in pages])
            for page in range(1, last_page + 1):
                next_page_url = f"http://macapa.ap.gov.br/page/{page}/"
                yield scrapy.FormRequest(
                    url=next_page_url,
                    method="GET",
                    formdata=params,
                    callback=self.parse,
                )
        yield from self.parse(response)

    def get_gazette_date(self, gazette):
        gazette_date = None
        raw_date = gazette.css("a h4::text").re_first(r"\d{2}\/\d{2}\/\d{4}")
        if raw_date:
            gazette_date = datetime.datetime.strptime(raw_date, "%d/%m/%Y").date()
        else:
            raw_date = gazette.css("a h4::text").re_first(r"(DE .*)") or ""
            gazette_date = dateparser.parse(raw_date)
            gazette_date = gazette_date.date() if gazette_date else None

        return gazette_date

    def parse(self, response):
        gazettes = response.css(".diary > .panel")
        for gazette in gazettes:
            gazette_url = gazette.css("a::attr(href)").get()
            edition_number = gazette.css(".panel-heading ::text").re_first(r"\d+")
            gazette_date = self.get_gazette_date(gazette)

            if gazette_date is not None and (
                gazette_date < self.start_date or gazette_date > self.end_date
            ):
                continue

            yield Gazette(
                date=gazette_date,
                file_urls=[gazette_url],
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive",
            )
