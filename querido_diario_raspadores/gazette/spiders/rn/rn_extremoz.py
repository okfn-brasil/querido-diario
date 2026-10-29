import datetime
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

MONTHS = {
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "marco": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}


class RnExtremozSpider(BaseGazetteSpider):
    TERRITORY_ID = "2403608"
    name = "rn_extremoz"
    allowed_domains = ["extremoz.rn.gov.br"]
    start_date = datetime.date(2013, 12, 17)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.start_date, str):
            self.start_date = datetime.datetime.strptime(
                self.start_date, "%Y-%m-%d"
            ).date()

    BASE_URL = "https://extremoz.rn.gov.br/diario-oficial"

    async def start(self):
        start_year = max(self.start_date.year, 2014)
        end_year = self.end_date.year
        for year in range(end_year, start_year - 1, -1):
            url = f"{self.BASE_URL}/diario-oficial-{year}/"
            yield scrapy.Request(url)
        if self.start_date.year <= 2013:
            url_older = f"{self.BASE_URL}/diario-oficial-anos-anteriores/"
            yield scrapy.Request(url_older)

    def parse(self, response):
        items = response.css("div.arq-list-item-content")
        for item in items:
            pdf_url = item.css("a::attr(href)").get()
            if not pdf_url:
                continue

            title = item.css("h1::text").get() or ""
            p_data = item.css("p.data::text").get() or ""
            gazette_date = self._parse_date(title, p_data)

            if not gazette_date:
                continue
            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                continue

            edition_match = re.search(
                r"(?:n[ºo°]|edi[çc][ãa]o)\s*(\d+)", title, re.IGNORECASE
            )
            edition_number = edition_match.group(1) if edition_match else ""

            is_extra_edition = any(
                term in title.lower() or term in pdf_url.lower()
                for term in ["extra", "especial"]
            )

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[response.urljoin(pdf_url)],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        if items:
            last_title = items[-1].css("h1::text").get() or ""
            last_p_data = items[-1].css("p.data::text").get() or ""
            last_date = self._parse_date(last_title, last_p_data)
            if last_date and last_date < self.start_date:
                return

        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def _parse_date(self, title, p_data):
        match_title = re.search(
            r"(\d{1,2})\s+de\s+([a-zA-Zç]+)\s+de\s+(\d{4})",
            title,
            re.IGNORECASE,
        )
        if match_title:
            day = int(match_title.group(1))
            month_name = match_title.group(2).lower()
            year = int(match_title.group(3))
            month = MONTHS.get(month_name)
            if month:
                try:
                    return datetime.date(year, month, day)
                except ValueError:
                    pass

        match_data = re.search(r"(\d{2})/(\d{2})/(\d{4})", p_data)
        if match_data:
            day, month, year = map(int, match_data.groups())
            try:
                return datetime.date(year, month, day)
            except ValueError:
                pass

        return None
