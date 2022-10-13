import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ApMacapaSpider(BaseGazetteSpider):

    name = "ap_macapa"
    allowed_domains = ["macapa.ap.gov.br"]
    start_date = None

    TERRITORY_ID = "1600303"

    def start_requests(self):
        base_url = "https://macapa.ap.gov.br/page/{page}/".format(**{"page": 1})
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
        )

    def _pagination_requests(self, response, page, start_date, end_date):
        pages = response.xpath("//a[@class='-numbers']/text()").getall()
        last_page = pages[-1] if pages else None
        if last_page:
            for next_page in range(1, last_page + 1):
                next_page_url = "https://macapa.ap.gov.br/page/{page}/".format(
                    **{"page": next_page}
                )
                params = {
                    "s": "",
                    "post_type": "official_diaries",
                    "search": "official_diaries",
                    "official_diary_initial_date": self.start_date,
                    "official_diary_final_date": self.end_date,
                }
                yield scrapy.FormRequest(
                    url=next_page_url,
                    method="GET",
                    formdata=params,
                    callback=self.parse,
                )

    def parse(self, response):
        # Extract Items
        extract_number_date = re.compile(
            r".+?(?P<num>\d{4}).+?(?P<date>\d\d/\d\d/\d\d\d\d)"
        )
        divs = response.xpath("//div[@class='panel-body']")[1:]
        for div in divs:
            url = div.xpath("./a/@href").get()
            text = div.xpath("./a/h4/text()").get()

            num_date = re.match(extract_number_date, text)
            edition_number = num_date.group("num")
            date = num_date.group("date")
            date = dateparser.parse(date, languages=["pt"]).date()
            yield Gazette(
                date=date,
                file_urls=[url],
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive",
            )
