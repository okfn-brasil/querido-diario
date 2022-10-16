import datetime as dt
import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ApMacapaSpider(BaseGazetteSpider):

    name = "ap_macapa"
    allowed_domains = ["macapa.ap.gov.br"]
    start_date = dt.datetime(2018, 1, 1)
    TERRITORY_ID = "1600303"

    def start_requests(self):
        base_url = "http://macapa.ap.gov.br/page/{page}/".format(**{"page": 1})
        start_date = self.start_date.strftime("%d/%m/%Y") if self.start_date else ""
        end_date = self.end_date.strftime("%d/%m/%Y") if self.end_date else ""
        self.logger.debug(f"Start Date: {start_date} End Date: {end_date}")
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
        last_page = int(pages[-1]) if pages else None
        if last_page:
            for next_page in range(1, last_page + 1):
                self.logger.debug(f"Page {next_page} of {last_page}")
                next_page_url = "http://macapa.ap.gov.br/page/{page}/".format(
                    **{"page": next_page}
                )
                yield scrapy.FormRequest(
                    url=next_page_url,
                    method="GET",
                    formdata=params,
                    callback=self.parse,
                )
        else:
            self.logger.debug("One page only")
            yield from self.parse(response)

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
