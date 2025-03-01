import re
from datetime import date

import dateparser
from fuzzywuzzy import process
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjCampoGoytacazesSpider(BaseGazetteSpider):
    name = "rj_campos_goytacazes"
    TERRITORY_ID = "3301009"
    allowed_domains = ["www.campos.rj.gov.br"]
    start_urls = ["https://www.campos.rj.gov.br/diario-oficial.php"]
    start_date = date(2013, 11, 1)
    months = [
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ]

    def parse(self, response):
        for element in response.css("ul.ul-licitacoes li"):
            gazette_data = element.css("h4::text")
            gazette_text = element.css("h4::text").get("")

            date = self.extract_date(gazette_text)
            if not date or date > self.end_date:
                continue
            if date < self.start_date:
                return

            edition_number = gazette_data.re_first(r"Edição.*\s(\d+)")

            path_to_gazette = element.css("a::attr(href)").get().strip()
            # From November 17th, 2017 and backwards the path to the gazette PDF
            # is relative.
            if path_to_gazette.startswith("up/diario_oficial.php"):
                path_to_gazette = response.urljoin(path_to_gazette)

            is_extra_edition = bool(
                re.search(r"extra|supl|revis", gazette_text, re.IGNORECASE)
            )

            yield Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[path_to_gazette],
                power="executive",
            )

        next_url = (
            response.css(".pagination")
            .xpath("//a[contains(text(), 'Proxima')]/@href")
            .get()
        )
        if next_url:
            yield Request(response.urljoin(next_url))

    def extract_date(self, text):
        """Extract a date from a text. This method attempts to correct typing errors in the month.

        Args:
            text: A text containing a date with the name of the month full version (%B)

        Returns:
            The date, if match. Otherwise, returns None.
        """

        match_date = re.search(r"\d{1,2}º?(\sde)? +(\w+)(\sde)? +\d{4}", text)
        if not match_date:
            return None

        raw_date = match_date.group(0)
        raw_date = raw_date.replace("º", "").replace("°", "")
        month = match_date.group(2)
        if month.lower() not in self.months:
            match_month, score = process.extractOne(month, self.months)
            if score < 70:
                return None
            raw_date = raw_date.replace(month, match_month)
            self.logger.warning(
                f' Erro de digitação em "{text}". CORRIGIDO DE {month} PARA {match_month}'
            )

        parsed_datetime = dateparser.parse(raw_date, languages=["pt"])
        return parsed_datetime.date() if parsed_datetime else None
