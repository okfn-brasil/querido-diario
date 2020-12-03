import re
from datetime import date, datetime

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrGuarapuavaSpider(BaseGazetteSpider):
    TERRITORY_ID = "4109401"
    name = "pr_guarapuava"
    allowed_domains = ["guarapuava.pr.gov.br"]
    start_urls = ["https://www.guarapuava.pr.gov.br/boletins-oficiais"]
    start_date = datetime(2002, 1, 20).date()

    def start_requests(self):
        todays_date = date.today()
        current_year = todays_date.year
        for year in range(current_year, self.start_date.year - 1, -1):
            url = f"https://www.guarapuava.pr.gov.br/boletins-oficiais/{year}-2/"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for gazette in response.css(".link > a"):
            link_str = gazette.css("a ::text").get()
            gazette_date = self.extract_gazette_date(link_str)

            if gazette_date is None:
                continue

            yield Gazette(
                date=gazette_date,
                file_urls=[gazette.css("a::attr(href)").extract_first()],
                power="executive",
                edition_number=self.extract_gazette_edition_number(link_str),
                is_extra_edition=self.gazzete_is_extra_edition(link_str),
            )

    def extract_gazette_date(self, text):
        matches = re.findall(r"(\d+/\d+/\d+)", text)

        if len(matches) == 0:
            return None

        return parse(matches[-1], languages=["pt"]).date()

    def extract_gazette_edition_number(self, text):
        match = re.search(r"Boletim(\s+)Oficial(\s+)(\d+)", text)

        if match is None:
            return None

        return match.group(0)

    def gazzete_is_extra_edition(self, text):
        return "extra" in text.lower()
