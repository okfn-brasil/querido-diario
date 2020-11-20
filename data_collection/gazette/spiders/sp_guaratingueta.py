import datetime
import re

import dateparser
import scrapy
from dateutil.rrule import YEARLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpGuaratinguetaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3518404"
    name = "sp_guaratingueta"
    allowed_domains = ["https://guaratingueta.sp.gov.br/"]
    start_date = datetime.date(2015, 6, 23)

    def start_requests(self):
        years = [
            r.year
            for r in rrule(
                freq=YEARLY, dtstart=self.start_date, until=datetime.date.today()
            )
        ]
        for year in years:
            if year == datetime.date.today().year:
                url = "https://guaratingueta.sp.gov.br/diario-oficial-da-estancia-turistica-de-guaratingueta/"
            else:
                url = f"https://guaratingueta.sp.gov.br/diario-oficial-{year}/"
            yield scrapy.Request(url)

    def parse(self, response):
        texts = response.xpath(
            '//*[@id="content"]/article/div[1]/ul/li/a//text()'
        ).getall()
        gazette_urls = response.xpath(
            '//*[@id="content"]/article/div[1]/ul/li/a/@href'
        ).getall()
        for gazette_url, text in zip(gazette_urls, texts):
            date = re.match("\d{2}\/\d{2}\/\d{4}", text).group()
            gazette_date = dateparser.parse(date, languages=["pt"]).date()
            file_urls = [gazette_url]
            is_extra_edition = (
                ("EXTRAORDINÁRIA" in text)
                or ("ESPECIAL" in text)
                or ("GABARITO" in text)
                or ("EXTRAORDINÁRIO" in text)
            )
            yield Gazette(
                date=gazette_date,
                file_urls=file_urls,
                is_extra_edition=is_extra_edition,
                power="executive",
            )
