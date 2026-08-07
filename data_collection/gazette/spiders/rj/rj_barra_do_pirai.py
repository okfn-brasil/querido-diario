import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjBarraDoPiraiSpider(BaseGazetteSpider):
    name = "rj_barra_do_pirai"
    TERRITORY_ID = "3300308"
    allowed_domains = ["transparencia.portalbarradopirai.com.br"]
    start_urls = [
        "https://transparencia.portalbarradopirai.com.br/index.php/pt/links/boletim-municipal"
    ]
    start_date = date(2009, 1, 7)

    def parse(self, response):
        year_links = response.xpath("//div[@itemprop='articleBody']//a/@href").getall()
        range_years = range(self.start_date.year, self.end_date.year + 1)
        for year_link in year_links:
            year = int(year_link[-4:])
            if year in range_years:
                yield scrapy.Request(
                    url=response.urljoin(year_link),
                    callback=self.parse_document,
                )

    def parse_document(self, response):
        gazette_links = response.xpath("//table[@class='easyfolderlisting ']//a")
        for gazette_link in gazette_links:
            raw_edition = gazette_link.xpath("./text()").get()
            date_tmp = re.search(r"Data\s+(\d{2}-\d{2})", raw_edition)
            if not date_tmp:
                continue

            year = response.url[-4:]
            date_tmp = date_tmp.group(1)
            date_tmp = f"{date_tmp}-{year}"
            date_tmp = dt.strptime(date_tmp, "%d-%m-%Y").date()

            if date_tmp > self.end_date:
                continue

            if date_tmp < self.start_date:
                return

            match = re.search(r"(\d+)", raw_edition)
            edition = match.group(0) if match else None
            extra = "extra" in raw_edition.lower()
            pdf_link = gazette_link.xpath(".//@href").get()
            if date_tmp <= date(2021, 10, 21):
                power_type = "executive"
            else:
                power_type = "executive_legislative"

            yield Gazette(
                date=date_tmp,
                edition_number=edition,
                is_extra_edition=extra,
                file_urls=[pdf_link],
                power=power_type,
            )
