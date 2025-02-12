import datetime
import locale
import logging
import re

from dateutil.relativedelta import relativedelta
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

logger = logging.getLogger(__name__)


class SpSaoCarlosSpider(BaseGazetteSpider):
    name = "sp_sao_carlos"
    TERRITORY_ID = "3548906"
    allowed_domains = ["saocarlos.sp.gov.br"]
    base_url = "http://www.saocarlos.sp.gov.br"
    start_date = datetime.date(2009, 5, 10)

    already_seen = set()

    class EndDateReached(Exception):
        pass

    def start_requests(self):
        year_diff = self.end_date.year - self.start_date.year
        month_diff = self.end_date.month - self.start_date.month
        months_between_start_and_end = year_diff * 12 + month_diff + 1
        dates_of_interest = (
            self.start_date + relativedelta(months=i)
            for i in range(months_between_start_and_end)
        )

        # For converting month names to Portuguese
        # Used in the URL generation and in the parsing of the gazette date
        try:
            locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        except locale.Error:
            locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

        def get_url(date_of_interest):
            year = date_of_interest.year
            month = date_of_interest.strftime("%B").lower().replace("ç", "c")
            return f"{self.base_url}/index.php/diario-oficial-{year}/diario-oficial-{month}-{year}.html"

        urls = map(get_url, dates_of_interest)
        yield from map(Request, urls)

    def find_gazette_rows(self, response):
        # Until May 2013, there was a single table with many rows
        rows_source = response.xpath(
            '//table[re:test(@style, "border-color: #dfdfe1|rgb\\(223, 223, 225\\)")]'
        )

        # From May 2013 onwards, they split the table into multiple single-row tables
        if len(rows_source) == 0:
            rows_source = response.xpath('//table[@width="620"]')

        if len(rows_source) > 0:
            gazette_rows = rows_source.xpath(".//tr")
            return gazette_rows

        logger.error("Could not find gazette data")

    def parse(self, response):
        gazette_rows = self.find_gazette_rows(response)

        for index, gazette_row in enumerate(gazette_rows):
            # Sometimes there are empty rows
            has_no_content = gazette_row is None
            if has_no_content:
                logger.warning(f"Empty row at index {index}")
                continue

            try:
                gazette = self.parse_gazette_row(gazette_row)
                if gazette:
                    yield gazette
            except self.EndDateReached:
                break

    def get_default_match(self, text):
        # Examples:
        # 'Edição nº 25 • Ano 1 • 1ºde agosto de 2009'
        # 'Edição n° 115 • Ano 1 •\xa0 27 defevereiro de 2010'
        # 'Edição nº 1898 • Ano 14\xa0• 1º de Fevereiro de 2022'
        pattern = r"n(?:º|°) (\d+).*Ano \d+.*?([1-3]?\d)º? ?de ?([A-zÀ-ú]+).*(\d{4})"
        matched = re.search(pattern, text)
        return matched

    def get_out_of_order_match(self, text):
        # Yes, this happens more than once
        # Examples:
        # 'Edição nº 901 • Ano 8\xa0• 01 Março de \xa0de 2016'
        # 'Edição nº 911 • Ano 8\xa0• 01 Abril de \xa0de 2016'
        pattern = r"n(?:º|°) (\d+).*Ano \d+.*?([1-3]?\d)º? ?([A-zÀ-ú]+).*(\d{4})"
        matched = re.search(pattern, text)
        return matched

    def parse_gazette_row(self, gazette_row):
        gazette_text = gazette_row.get()
        matched = self.get_default_match(gazette_text)

        if not matched:
            matched = self.get_out_of_order_match(gazette_text)

        if not matched:
            logger.error(
                "Gazzette text does not match any known patterns", gazette_text
            )
            return None

        edition_number = matched.group(1)
        if edition_number in self.already_seen:
            raise ValueError(f"Duplicate edition number: {edition_number}")
        self.already_seen.add(edition_number)
        day = matched.group(2)
        month = matched.group(3)
        year = matched.group(4)
        date = datetime.datetime.strptime(f"{day} {month} {year}", "%d %B %Y").date()

        if date < self.start_date:
            return None

        if date > self.end_date:
            raise self.EndDateReached(f"End date reached: {date}")

        extra = "(extra)" in gazette_text

        file_url = gazette_row.xpath(".//a/@href").get()

        if not file_url.startswith("http"):
            file_url = f"{self.base_url}{file_url}"

        return Gazette(
            edition_number=edition_number,
            date=date,
            file_url=file_url,
            file_urls=[file_url],
            is_extra_edition=extra,
            power="executive",
        )
