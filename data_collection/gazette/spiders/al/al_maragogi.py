import re
from datetime import date, datetime

import scrapy
from dateutil.rrule import YEARLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AlMaragogiSpider(BaseGazetteSpider):
    name = "al_maragogi"
    TERRITORY_ID = "2704500"
    allowed_domains = ["maragogi.al.gov.br"]
    base_url = "https://maragogi.al.gov.br/diarios-oficiais/diario-oficial-"
    start_urls = ["https://maragogi.al.gov.br/diarios-oficiais/"]
    start_date = date(2020, 1, 1)
    end_date = date.today()
    stop_crawling = False

    def extrair_numero(self, arquivo):
        match = re.search(r"no-(\d+)-", arquivo)
        if match:
            return match.group(1)
        return None

    def start_requests(self):
        for date_of_interest in rrule(
            freq=YEARLY, dtstart=self.start_date, until=self.end_date
        ):
            base_url = f"{self.base_url}{date_of_interest.year}/"
            yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):
        if self.stop_crawling:
            return

        titles = response.css(".arq-list-item-content h1::text").getall()
        dates = response.css(".data::text").getall()

        for title, data_str in zip(titles, dates):
            edition_number = self.extrair_numero(title)
            data_str = data_str.strip()

            try:
                item_date = datetime.strptime(data_str, "%d/%m/%Y").date()
            except ValueError:
                continue

            if item_date < self.start_date:
                self.stop_crawling = True
                return

            if title.endswith("."):
                title = title[:-1]

            if not title.endswith(".pdf"):
                title += ".pdf"

            file_url = f"https://maragogi.al.gov.br/wp-content/uploads/{item_date.year}/{item_date.month:02d}/{title}"

            yield Gazette(
                date=item_date,
                edition_number=edition_number,
                is_extra_edition=False,
                file_urls=[file_url],
                power="executive",
            )

        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
