import calendar
import re
from datetime import date
from string import punctuation

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

EDITION_NUMBER_RE = re.compile(r"Edição\s+(?:Extra\s+)?-?\s*(\d+)")
REGULAR_FULL_NOMINAL_DATE_RE = re.compile(
    r"\s+"
    r"(\d{1,2})(?# day)"
    r"\s+d?e?\s*"
    rf"([^\d\s{punctuation}]+)(?# nominal month in pt)"
    r"\s+d?e?\s*"
    r"(\d{4})(?# year)",
    flags=re.IGNORECASE,
)
MONTH_YEAR_NOMINAL_DATE_RE = re.compile(
    r"Oficial\s+de\s*"
    rf"([^\d\s{punctuation}]+)(?# nominal month in pt)"
    r"\s+d?e?\s*"
    r"(\d{4})(?# year)",
    flags=re.IGNORECASE,
)


class RjCamposDosGoytacazesSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301009"

    allowed_domains = ["www.campos.rj.gov.br"]
    name = "rj_campos_dos_goytacazes"

    start_date = date(2010, 6, 10)
    # November 17th, 2017 was the date of the last Diário Oficial gazette and
    # also the date of the first Diário Oficial Eletrônico gazette

    BASE_URL = (
        "https://www.campos.rj.gov.br/diario-oficial.php"
        "?PGpagina={PAGE_NUMBER}&PGporPagina=15"
    )
    start_urls = [BASE_URL.format(PAGE_NUMBER=1)]

    def __init__(self, *args, **kwargs):
        super(RjCamposDosGoytacazesSpider, self).__init__(*args, **kwargs)
        self.current_date = None
        self.current_edition_number = ""
        self.row_texts = set()

        # Given that there are some gazettes with multiple rows, and they can be
        # spread across subsequent pages, we temporarily store data, which is consumed
        # once we confirm a differente date found for the next row in the page.
        #
        # That storage is a dict in which the key a bool value for is_extra_edition
        # and each dict entries' value is a list of URLs associated to that gazette date
        # and its is_extra_edition value.
        #
        # Example for 2018-05-05:
        # collected_data_for_current_date = {
        #     False: [https://www.campos.rj.gov.br/app/assets/diario-oficial/link/2540],
        #     True: [https://www.campos.rj.gov.br/app/assets/diario-oficial/link/2542],
        # }
        self.collected_data_for_current_date = {}

    @staticmethod
    def extract_date_from_regular_full_nominal_date(match_):
        textual_date = f"{match_.group(1)} de {match_.group(2)} de {match_.group(3)}"
        gazette_date = dateparser.parse(textual_date, languages=["pt"]).date()
        return gazette_date

    @staticmethod
    def extract_date_from_month_year_nominal_date(match_):
        # To avoid any issues for the date conversion, we do a safe replacement to
        # initially consider as the first day of the month
        textual_date = f"01 de {match_.group(1)} de {match_.group(2)}"
        gazette_date = dateparser.parse(textual_date, languages=["pt"]).date()

        # As this case is a collection of gazettes for the full month,
        # we consider the gazette date as the last day of that month
        last_day_of_the_month = calendar.monthrange(
            year=gazette_date.year, month=gazette_date.month
        )[1]
        gazette_date = gazette_date.replace(day=last_day_of_the_month)

        return gazette_date

    def extract_date_from_gazette_text(self, gazette_text):
        if not gazette_text:
            return None

        text = (
            gazette_text
            # The extra edition for August 28th, 2018 has a typo in the month name.
            .replace("Agosoto", "Agosto")
            # The edition for December 17th, 2012 has a typo in the month name.
            .replace("Dezembrbo", "Dezembro")
        )

        if match_ := REGULAR_FULL_NOMINAL_DATE_RE.search(text):
            return self.extract_date_from_regular_full_nominal_date(match_)

        # From October 2012 to October 2013, it has a single row per month
        # The provided data is a rar extension file and some of them are missing
        if match_ := MONTH_YEAR_NOMINAL_DATE_RE.search(text):
            return self.extract_date_from_month_year_nominal_date(match_)

        self.logger.warning(f"No date could be extracted from '{text}'")
        return None

    def triage_data_per_row(self, gazette_text):
        """Triage gazette data for a gazette that is from November 17th 2017 or earlier.

        It returns a 3-tuple:
            the extracted gazette date,
            whether it is an extra edition, and
            the edition number when applicable.
        """
        gazette_date = None
        is_extra_edition = (
            gazette_text.startswith("Suplemento") or "Extra" in gazette_text
        )
        edition_number = ""

        if not gazette_text:
            return gazette_date, is_extra_edition, edition_number

        gazette_date = self.extract_date_from_gazette_text(gazette_text)
        if (
            not gazette_date
            or gazette_date < self.start_date
            or self.end_date < gazette_date
        ):
            return gazette_date, is_extra_edition, edition_number

        edition_number_match = EDITION_NUMBER_RE.search(gazette_text)
        if edition_number_match:
            edition_number = edition_number_match.group(1).strip()

        return gazette_date, is_extra_edition, edition_number

    def instantiate_gazettes_and_reset_stored_data(self):
        """Instantiates Gazette from the most recent data and resets the state."""

        if not self.current_date:
            return []

        gazettes = [
            Gazette(
                date=self.current_date,
                edition_number=str(self.current_edition_number),
                file_urls=file_urls,
                is_extra_edition=is_extra_edition,
                power="executive",
            )
            for (
                is_extra_edition,
                file_urls,
            ) in self.collected_data_for_current_date.items()
        ]

        self.current_date = None
        self.current_edition_number = ""
        self.collected_data_for_current_date = {}
        return gazettes

    def parse(self, response):
        """Triage gazette data from a page row.

        Once we notice that either the edition_number or the gazette_date changed
        between rows, we collect the gazettes.

        Otherwise, we triage from the next page.
        """

        is_gazette_date_before_start_date = False
        for row_element in response.css("ul.ul-licitacoes li"):
            gazette_text = row_element.css("h4::text").get("").strip()
            file_url = row_element.css("a::attr(href)").get().strip()

            if not gazette_text or not file_url:
                continue

            if gazette_text in self.row_texts:
                self.logger.info(
                    f"Textual value '{gazette_text}' was already processed earlier"
                )
                continue

            gazette_date, is_extra_edition, edition_number = self.triage_data_per_row(
                gazette_text
            )

            if not gazette_date or self.end_date < gazette_date:
                continue

            if gazette_date < self.start_date:
                is_gazette_date_before_start_date = True
                break

            if (
                self.current_edition_number != edition_number
                or self.current_date != gazette_date
            ):
                yield from self.instantiate_gazettes_and_reset_stored_data()

            self.row_texts.add(gazette_text)
            self.current_edition_number = edition_number
            self.current_date = gazette_date
            self.collected_data_for_current_date.setdefault(
                is_extra_edition, []
            ).append(file_url)

        next_url = (
            response.css(".pagination")
            .xpath("//a[contains(text(), 'Proxima')]/@href")
            .get()
        )

        if is_gazette_date_before_start_date or not next_url:
            # Collect the gazettes using the triaged data
            #
            # Regarding the `not next_url` condition, due to the Gazette instantiation
            # construct of this spider, this is a corner case when we collect without
            # an explicit start_date, meaning that is_gazette_date_before_start_date
            # wouldn't be set to True
            yield from self.instantiate_gazettes_and_reset_stored_data()
        else:
            # Keep triaging data
            yield Request(response.urljoin(next_url))
