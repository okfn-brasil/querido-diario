import re
from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RJMiracemaSpider(BaseGazetteSpider):
    name = "rj_miracema"
    TERRITORY_ID = "3303005"
    allowed_domains = ["miracema.rj.gov.br", "miracema.plugtecnologia.com.br"]
    start_urls = [
        "https://www.miracema.rj.gov.br/transparencia/exibir/20/0/1/boletim-oficial"
    ]
    start_date = date(2017, 1, 15)

    def parse(self, response):
        for tr in response.css("tbody tr"):
            year_text = tr.css("td::text").get()
            if not year_text:
                continue

            try:
                year = int(year_text.strip())
            except ValueError:
                continue

            if self.start_date.year <= year <= self.end_date.year:
                url = tr.css('a[title="Abrir pasta"]::attr(href)').get()
                if url:
                    yield scrapy.Request(url=url, callback=self.gazette_parse)

    def gazette_parse(self, response):
        data = response.css("table.table.table-striped.table-sm.mb-0 tbody tr")

        for edition in data:
            edition_text = edition.css("td::text").get()
            if "boleti" in edition_text.lower():
                continue

            match = re.search(r"\d{2}\.\d{2}\.\d{4}", edition_text)

            if match:
                edition_date = datetime.strptime(match.group(), "%d.%m.%Y").date()

            if not self.start_date <= edition_date <= self.end_date:
                continue

            edition_url = edition.css(
                'a[title="Download do arquivo"]::attr(href)'
            ).get()

            extra_edition = "parte" in edition_text.lower() or re.search(
                r"\b\d{3}[A-Za-z]\b", edition_text
            )

            num = re.search(r"B\.O\s+(\d+)", edition_text)

            if num:
                edition_number = num.group(1)

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                is_extra_edition=extra_edition,
                file_urls=[edition_url],
                power="executive",
            )

        current_page = int(response.url.split("/")[7])
        pages = response.css("li.page-item span::text").getall()

        if pages:
            last_page = int(pages[-2])
            if current_page < last_page:
                next_page = current_page + 1
                next_url = response.url.replace(f"/{current_page}/", f"/{next_page}/")
                yield scrapy.Request(url=next_url, callback=self.gazette_parse)
