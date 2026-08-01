from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjAngraDosReisSpider(BaseGazetteSpider):
    name = "rj_angra_dos_reis"
    TERRITORY_ID = "3300100"
    allowed_domains = ["angra.rj.gov.br"]
    start_date = date(2005, 3, 11)
    start_urls = ["https://angra.rj.gov.br/boletim-oficial"]

    def parse(self, response):
        for tr in response.xpath("//article//tr")[1:]:
            raw_gazette_date = tr.xpath("./td[1]/text()").get()
            gazette_date = dt.strptime(raw_gazette_date, "%d/%m/%Y").date()
            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            gazette_edition_number = tr.xpath("./td[3]/text()").get()

            url_subdir = tr.xpath(".//a/@href").get()
            gazette_url = response.urljoin(url_subdir)

            gazette_type = tr.xpath("./td[4]/text()").get()
            is_extra_edition = "EXTRA" in f"{gazette_type}{url_subdir}".upper()

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive_legislative",
            )

        next_page = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if next_page:
            yield scrapy.Request(next_page)
