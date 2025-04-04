import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class RjMaricaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3302700"
    name = "rj_marica"
    allowed_domains = ["marica.rj.gov.br"]
    start_date = date(2006, 7, 17)
    BASE_URL = "https://www.marica.rj.gov.br/wp-admin/admin-ajax.php"

    def start_requests(self):
        for monthly_date in monthly_sequence(self.start_date, self.end_date):
            for gazette_type in ["jom", "jom-especial"]:
                yield scrapy.FormRequest(
                    method="GET",
                    url=self.BASE_URL,
                    formdata={
                        "post_type": gazette_type,
                        "year": str(monthly_date.year),
                        "month": str(monthly_date.month),
                        "action": "alm_get_posts",
                        "posts_per_page": "31",
                    },
                )

    def parse(self, response):
        html = response.json()["html"]
        if html:
            gazette_list = html.split("\n\n\n")
            for gazette_data in gazette_list[:-1]:
                raw_gazette_date = re.search(r"\d+\/\d+\/\d+", gazette_data).group()
                gazette_date = dt.strptime(raw_gazette_date, "%d/%m/%Y").date()
                if not self.start_date <= gazette_date <= self.end_date:
                    continue

                gazette_edition_number = re.search(
                    r'title=".*?(\d+)"', gazette_data
                ).group(1)

                gazette_item = {
                    "date": gazette_date,
                    "edition_number": gazette_edition_number,
                }

                gazette_url = re.search(r'href="(.*?)"', gazette_data).group(1)
                yield scrapy.Request(
                    gazette_url,
                    callback=self.parse_gazette,
                    cb_kwargs={"gazette_item": gazette_item},
                )

    def parse_gazette(self, response, gazette_item):
        gazette_url = response.xpath('//*[@class="vc_btn3-container"]//a/@href').get()
        if gazette_url is not None:
            yield Gazette(
                **gazette_item,
                file_urls=[gazette_url],
                power="executive_legislative",
                is_extra_edition="jom-especial" in response.url
            )
