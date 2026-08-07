import re
from datetime import date

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjPetropolis(BaseGazetteSpider):
    name = "rj_petropolis"
    TERRITORY_ID = "3303906"
    allowed_domains = ["petropolis.rj.gov.br"]
    start_urls = [
        "https://www.petropolis.rj.gov.br/pmp/index.php/servicos-cidadao/diario-oficial"
    ]
    start_date = date(2001, 10, 2)

    def parse(self, response):
        for a in response.xpath("//div[@class='col-2 text-center']//p/a"):
            year = int(a.xpath("./text()").get())
            if self.start_date.year <= year <= self.end_date.year:
                url = a.xpath("./@href").get()
                base_url = response.urljoin(url)
                yield scrapy.Request(
                    url=base_url,
                    callback=self.parse_year_month,
                    cb_kwargs={"year": year},
                )

    def parse_year_month(self, response, year):
        for a in response.xpath("//div[@class='col-2 text-center']//p/a"):
            url = a.xpath("./@href").get()
            gazette_month_name = a.xpath("./text()").get()
            gazette_month = dateparser.parse(gazette_month_name).month
            month_start = self.start_date.replace(day=1)
            month_end = self.end_date.replace(day=1)
            month = date(year, gazette_month, 1)
            if month_start <= month <= month_end:
                base_url = response.urljoin(url)
                yield scrapy.Request(
                    url=base_url,
                    callback=self.parse_gazette,
                    cb_kwargs={"year": year, "month": gazette_month},
                )

    def parse_gazette(self, response, month, year):
        tr_xpath = "//table[contains(@class, 'tabela-do')]/tbody/tr"
        for gazette_data in response.xpath(tr_xpath):
            raw_gazette_name = (
                gazette_data.xpath("./th/a/text()")
                .get()
                .replace("º", "")
                .replace("°", "")
            )

            raw_gazette_date = re.search(
                r"\s(\d{1,2}\s)(.*?\d{4}|/\d{1,2}/\d{2,4})", raw_gazette_name
            )
            if raw_gazette_date is None or not raw_gazette_date.group(1):
                continue

            day = int(raw_gazette_date.group(1))
            gazette_date = date(year, month, day)
            if not self.start_date <= gazette_date <= self.end_date:
                continue

            url_subdir = gazette_data.xpath("./th/a/@href").get()
            gazette_url = response.urljoin(url_subdir)

            gazette_edition_number = (
                gazette_data.xpath("./td[1]/p").re_first(r"\d+") or ""
            )

            is_extra_edition = bool(
                re.search(r"supl|extra", raw_gazette_name, re.IGNORECASE)
            )

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive",
            )
