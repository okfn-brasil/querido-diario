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
    allowed_domains = ["guaratingueta.sp.gov.br"]
    start_date = datetime.date(2015, 6, 23)

    def start_requests(self):
        years = [
            frequency.year
            for frequency in rrule(
                freq=YEARLY, dtstart=self.start_date, until=datetime.date.today()
            )
        ]
        for year in years:
            if year == datetime.date.today().year:
                url = "https://guaratingueta.sp.gov.br/diario-oficial-da-estancia-turistica-de-guaratingueta/"
            else:
                url = f"https://guaratingueta.sp.gov.br/diario-oficial-{year}/"
            yield scrapy.Request(url, meta={"current_year": year})

    def parse(self, response):
        texts = response.xpath(
            "//div[1]/div/div/div[1]/div/article/div[1]/ul/li"
        ).getall()
        texts = [self._clean_edition_text(edition_title) for edition_title in texts]

        gazette_urls = response.xpath(
            "//div[1]/div/div/div[1]/div/article/div[1]/ul/li/a[1]/@href"
        ).getall()
        for gazette_url, text in zip(gazette_urls, texts):
            # year needs to be 3 or 4 because of typos
            date = re.match(r"[0-9]{2}/[0-9]{2}/\s?[0-9]{3,4}", text).group()
            if len(date) < 10:
                date = self._handle_date_typos(date, response.meta.get("current_year"))
            gazette_date = dateparser.parse(date, languages=["pt"]).date()
            file_urls = [gazette_url]
            is_extra_edition = any(
                [
                    word in text
                    for word in [
                        "EXTRAORDINÁRIA",
                        "ESPECIAL",
                        "GABARITO",
                        "EXTRAORDINÁRIO",
                    ]
                ]
            )
            yield Gazette(
                date=gazette_date,
                file_urls=file_urls,
                is_extra_edition=is_extra_edition,
                power="executive",
            )

    def _clean_edition_text(self, edition_title):
        # use uppercase
        edition_title = edition_title.upper()
        # remove HTML tags
        edition_title = re.sub(r"<.*?>", "", edition_title)
        # remove weird character \xa0
        edition_title = edition_title.replace("\xa0", "")
        # replace 'O' with 0 (zero) in date
        edition_title = edition_title[:10].replace("O", "0") + edition_title[10:]
        return edition_title

    def _handle_date_typos(self, date, current_year):
        date_components = date.split("/")
        # handle year typo (e.g: '16/07/208' in https://guaratingueta.sp.gov.br/diario-oficial-2018/)
        if len(date_components[2]) != 4:
            date_components[2] = str(current_year)
        return "/".join(date_components)
