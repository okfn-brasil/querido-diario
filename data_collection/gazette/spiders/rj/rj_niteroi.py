import datetime as dt

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import daily_sequence


class RjNiteroiSpider(BaseGazetteSpider):
    TERRITORY_ID = "3303302"
    name = "rj_niteroi"
    allowed_domains = ["niteroi.rj.gov.br"]
    BASE_URL = "https://diariooficial.niteroi.rj.gov.br"
    start_date = dt.date(2003, 7, 1)

    month_names = [
        "01_Jan",
        "02_Fev",
        "03_Mar",
        "04_Abr",
        "05_Mai",
        "06_Jun",
        "07_Jul",
        "08_Ago",
        "09_Set",
        "10_Out",
        "11_Nov",
        "12_Dez",
    ]

    def start_requests(self):
        for date in daily_sequence(self.start_date, self.end_date):
            month = self.month_names[date.month - 1]
            year = date.year
            day = date.day

            yield Request(
                f"{self.BASE_URL}/do/{year}/{month}/{day:02d}.pdf",
                cb_kwargs={"gazette_date": date.date()},
            )

    def parse(self, response, gazette_date):
        yield Gazette(
            date=gazette_date,
            is_extra_edition=False,
            file_urls=[response.url],
            power="executive",
        )
