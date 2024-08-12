import re
from datetime import date, datetime as dt

import scrapy
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjMaricaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3302700"
    name = "rj_marica"
    allowed_domains = ["marica.rj.gov.br"]
    start_date = date(2006, 7, 17)
    BASE_URL = "https://www.marica.rj.gov.br/wp-admin/admin-ajax.php?slug={GAZETTE_TYPE}&post_type={GAZETTE_TYPE}&year={YEAR}&month={MONTH}&action=alm_get_posts&order=DESC&orderby=date&posts_per_page=31"

    def start_requests(self):
        end_date = self.end_date + relativedelta(months=1)
        for monthly_date in rrule(
            freq=MONTHLY, dtstart=self.start_date, until=end_date
        ):
            year = monthly_date.strftime("%Y")
            month = monthly_date.strftime("%m")
            for gazette_type in ["jom", "jom-especial"]:
                base_url = self.BASE_URL.format(
                    GAZETTE_TYPE=gazette_type, YEAR=year, MONTH=month
                )
                yield scrapy.FormRequest(
                    method="GET",
                    url=base_url,
                )

    def parse(self, response):
        html = response.json()["html"]
        if html:
            gazette_list = html.split("\n\n\n")
            for gazette_data in gazette_list[0:-1]:
                raw_gazette_date = re.search(r"\d+\/\d+\/\d+", gazette_data).group(0)
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
                    method="GET",
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
