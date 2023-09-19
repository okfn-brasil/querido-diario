from datetime import datetime, date
import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PaAnanindeuaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1500800"
    name = "pa_ananindeua"
    allowed_domains = ["ananindeua.pa.gov.br"]
    URL_BASE = "https://www.ananindeua.pa.gov.br"
    NUMBER_REGEX = re.compile(r"DI[AÁ]RIO N.\s*(\d+)", re.IGNORECASE)
    DATE_REGEX = re.compile(r"Data da Publicação: (.+)", re.IGNORECASE)
    start_date = date(2008, 12, 1)

    def start_requests(self):
        url = f"{self.URL_BASE}/diario_oficial?titulo=&dataini={self.start_date}&datafim={self.end_date}&order=1&go=Buscar&bt_buscar=buscar"
        yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # pagination
        next_page_url = response.css("div#pgnav_next>a::attr(href)").get()
        if next_page_url != None:
            yield scrapy.Request(
                f"{self.URL_BASE}{next_page_url}", callback=self.parse_page
            )
        # gazettes on page
        all_gazette_cards = response.css("div.item_lic")
        for gazette_card in all_gazette_cards:
            card_title = gazette_card.css("div>div::text").get().strip()
            match = self.NUMBER_REGEX.search(card_title)
            if match:
                gazette_number = match.group(1)
            else:
                gazette_number = ""
            gazette_date = self.DATE_REGEX.search(
                gazette_card.css("div>div>div::text").get().strip()
            ).group(1)
            gazette_date = dateparser.parse(
                gazette_date, settings={"DATE_ORDER": "DMY"}
            )
            gazette_date = gazette_date.date()
            url = gazette_card.css("a::attr(href)").get()
            gazette_url = f"{self.URL_BASE}{url}"

            yield Gazette(
                date=gazette_date,
                edition_number=gazette_number,
                file_urls=[gazette_url],
                is_extra_edition="extra" in card_title.lower(),
                territory_id=self.TERRITORY_ID,
                scraped_at=datetime.utcnow(),
                power="executive",
            )
