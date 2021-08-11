import datetime
import re

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class GoGoianiaSpider(BaseGazetteSpider):
    TERRITORY_ID = "5208707"
    name = "go_goiania"
    allowed_domains = ["goiania.go.gov.br"]
    start_urls = ["http://www4.goiania.go.gov.br/portal/site.asp?s=775&m=2075"]
    start_date = datetime.date(1960, 4, 21)

    def start_requests(self):
        initial_year = self.start_date.year
        end_year = datetime.date.today().year
        for year in range(initial_year, end_year + 1):
            yield scrapy.Request(
                f"http://www.goiania.go.gov.br/shtml//portal/casacivil/lista_diarios.asp?ano={year}"
            )

    def parse(self, response):
        gazettes = response.css("a")
        for gazette in gazettes:
            gazette_info = gazette.css("::text").re(
                r"Edi..o\s*n.\s*(\d+) de (\d{2}) de (.*?) de (\d{4})"
            )
            if not gazette_info:
                self.logger.warning(
                    f"Unable to identify gazette info for {response.url}."
                )
                continue

            edition_number, day, month, year = gazette_info
            gazette_date = parse(f"{day} de {month} de {year}", languages=["pt"]).date()
            if gazette_date < self.start_date:
                continue

            gazette_url = response.urljoin(gazette.css("::attr(href)").get())

            link_text = gazette.css("::text").get().lower()
            is_extra_edition = bool(
                re.search(r"suplemento|complemento|especial", link_text)
            )

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                power="executive",
            )
