import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjNiteroiSpider(BaseGazetteSpider):
    TERRITORY_ID = "3303302"
    name = "rj_niteroi"
    allowed_domains = ["niteroi.rj.gov.br"]
    start_urls = ["http://www.niteroi.rj.gov.br"]
    download_url = "http://pgm.niteroi.rj.gov.br/downloads/do/{}/{}/{:02d}.pdf"
    start_date = None
    end_date = None

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        self.start_date = dt.date(2003, 7, 1)
        self.end_date = dt.date.today()

        super(RjNiteroiSpider, self).__init__(start_date, end_date)

        self.logger.debug(
            "Start date is {date}".format(date=self.start_date.isoformat())
        )
        self.logger.debug("End date is {date}".format(date=self.end_date.isoformat()))

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

    def parse(self, response):
        parsing_date = self.end_date
        while parsing_date >= self.start_date:
            month = self.month_names[parsing_date.month - 1]
            url = self.download_url.format(parsing_date.year, month, parsing_date.day)
            yield scrapy.Request(
                url,
                method="HEAD",
                callback=self.parse_valid_gazette_file,
                cb_kwargs={"gazette_date": parsing_date},
            )
            parsing_date = parsing_date - dt.timedelta(days=1)

    def parse_valid_gazette_file(self, response, gazette_date):
        yield Gazette(
            date=gazette_date,
            file_urls=[response.url],
            is_extra_edition=False,
            power="executive",
        )
