from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjAngraDosReisSpider(BaseGazetteSpider):
    name = "rj_angra_dos_reis"
    TERRITORY_ID = "3300100"
    allowed_domains = ["angra.rj.gov.br"]
    start_date = date(2005, 3, 11)

    def start_requests(self):
        for year in range(self.start_date.year, self.end_date.year + 1):
            yield scrapy.Request(
                f"https://angra.rj.gov.br/boletim-oficial.asp?vAno={year}"
            )

    def parse(self, response):
        for tr in response.xpath("//article//tr")[1:]:
            raw_gazette_date = tr.xpath("./td/strong/text()").get()
            gazette_date = dt.strptime(raw_gazette_date, "%d/%m/%Y").date()
            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            raw_gazette_edition = tr.xpath("./td/text()")
            gazette_edition_number = raw_gazette_edition.re_first(r"\d+") or ""

            url_subdir = tr.xpath(".//a/@href").get()
            gazette_url = response.urljoin(url_subdir)

            is_extra_edition = (
                "EXTRA" in (raw_gazette_edition.get() + url_subdir).upper()
            )

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive_legislative",
            )
