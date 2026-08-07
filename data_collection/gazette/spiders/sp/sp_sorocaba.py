import re
from datetime import date, datetime
from string import punctuation

import dateparser
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

MONTH_STR = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Marco",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


EDITION_NUMBER_RE = re.compile(r"^\s*([0-9.]+)\s*[-–]\s*")
REGULAR_FULL_NOMINAL_DATE_RE = re.compile(
    r"^\s*"
    r"(\d{1,2})(?# day)"
    r"\s+d?e?\s*"
    rf"([^\d\s{punctuation}]+)(?# nominal month in pt)"
    r"(?:\s+d?e?\s*|-)"
    r"(\d{4})(?# year)"
    r"\s*[-–]*\s*",
    flags=re.IGNORECASE,
)
ALTERNATIVE_REGULAR_FULL_NOMINAL_DATE_RE = re.compile(
    r"\s*[-–]*\s*"
    r"(\d{1,2})(?# day)"
    r"\s+d?e?\s*"
    rf"([^\d\s{punctuation}]+)(?# nominal month in pt)"
    r"(?:\s+d?e?\s*|-)"
    r"(\d{4})(?# year)",
    flags=re.IGNORECASE,
)
DAY_MONTH_NOMINAL_DATE_RE = re.compile(
    r"^\s*"
    r"(\d{1,2})(?# day)"
    r"\s+d?e?\s*"
    rf"([^\d\s{punctuation}]+)(?# nominal month in pt)"
    r"\s*[-–]*\s*"
    r"(?!d?e?\s*\d{4})(?# for this pattern it cannot match the year component)",
    flags=re.IGNORECASE,
)
# Matches 'parte-\d' from 2006-12-28, 'part\d' from 2012-02-10, and
# 'Parte \d' from many other days
REGULAR_GAZETTE_PART_RE = re.compile(r"^Parte?(?:\s*|-)\d+$", flags=re.IGNORECASE)


class SpSorocabaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3552205"
    name = "sp_sorocaba"
    allowed_domains = ["noticias.sorocaba.sp.gov.br"]
    BASE_URL = "https://noticias.sorocaba.sp.gov.br/jornal/"

    # At 2022-12-31, the earliest gazette available was 1.132 from January 7th 2005
    start_date = date(2005, 1, 7)  # edition_number 1.132

    def __init__(self, *args, **kwargs):
        super(SpSorocabaSpider, self).__init__(*args, **kwargs)

        # The system that provides the gazettes for this territory is split into
        # year-month combinations.
        #
        # To keep data split into those periods, in the dict, we use a date value
        # representing the year-month combination as key and a dict for its value.
        #
        # The value dict has the edition_number as its key and a list of 2-tuple as its value:
        # the 0-index is the gazette-date and
        # the 1-index is a dict that uses extra_text as its key and holds a URL as its value.
        #
        # Example:
        # data_by_monthly_date_by_edition_number = {
        #     date(2019, 4, 1): {
        #         "2249": [
        #             (
        #                 date(2019, 4, 26),
        #                 {
        #                     "": "http://noticias.sorocaba.sp.gov.br/wp-content/uploads/2019/12/agencia-teste-2249-26-de-abril-de-2019.pdf",
        #                     "SISTEMA DE EVOLUCAO FUNCIONAL – EDITAL 01 2019 SAAE": "http://noticias.sorocaba.sp.gov.br/wp-content/uploads/2019/12/agencia-teste-2249-26-de-abril-de-2019-sistema-de-evolucao-funcional-edital-01-2019-saae.pdf",
        #                     "ENQUADRAMENTO DA EVOLUCAO FUNCIONAL – EDITAL SERH GS – 01 2019": "http://noticias.sorocaba.sp.gov.br/wp-content/uploads/2019/12/agencia-teste-2249-26-de-abril-de-2019-enquadramento-da-evolucao-funcional-edital-serh-gs-01-2019.pdf",
        #                 },
        #             ),
        #         ]
        #     }
        # }

        self.data_by_monthly_date_by_edition_number = {}

    def start_requests(self):
        # There are some gazettes that were placed in the immediately preceding month,
        # so we will search for a month before the start_date and a month after
        # the end_date
        if SpSorocabaSpider.start_date < self.start_date:
            first_of_the_month_before_start_date = self.start_date.replace(
                day=1
            ) - relativedelta(months=1)
            local_start_date = first_of_the_month_before_start_date
            self.logger.info(
                f"As we are querying a custom period, we will also query"
                f" {local_start_date.strftime('%Y-%m')} which may also include"
                f" some gazettes from {self.start_date.isoformat()} onwards"
            )
        else:
            local_start_date = self.start_date.replace(day=1)

        local_end_date = self.end_date
        if self.end_date < date.today().replace(day=1):
            one_month_after_end_date = self.end_date.replace(day=1) + relativedelta(
                months=1
            )
            local_end_date = one_month_after_end_date
            self.logger.info(
                f"As we are querying a custom period, we will also query"
                f" {local_end_date.strftime('%Y-%m')} which may also include"
                f" some gazettes until {self.end_date.isoformat()}"
            )

        # We store year-month tuples to handle the irregular cases
        requested_year_month = set()

        for monthly_date in rrule(
            freq=MONTHLY,
            dtstart=local_start_date,
            until=local_end_date,
        ):
            requested_year_month.add(monthly_date.timetuple()[:2])
            url = (
                f"{self.BASE_URL}"
                f"?ano={monthly_date.year}%20{MONTH_STR[monthly_date.month]}"
            )
            yield Request(
                url=url,
                callback=self.triage_data_per_page,
                cb_kwargs={"monthly_date": monthly_date, "page_number": 1},
            )

        for monthly_date in self.calculate_extra_requests(requested_year_month):
            url = (
                f"{self.BASE_URL}"
                f"?ano={monthly_date.year}%20{MONTH_STR[monthly_date.month]}"
            )
            yield Request(
                url=url,
                callback=self.triage_data_per_page,
                cb_kwargs={"monthly_date": monthly_date, "page_number": 1},
            )

    def calculate_extra_requests(
        self,
        requested_year_month,  # a set of year-month combination to extract irregular gazettes
    ):
        # Special cases: 3 editions are found only when querying
        # the same expected month from a year earlier
        # - regular gazette for edition_number 2658 of 2021-01-11 found querying 2020-01
        # - regular gazette for edition_number 2986 of 2022-05-17 found querying 2021-05
        # - regular gazette for edition_number 2987 of 2022-05-18 found querying 2021-05
        irregular_placing_map = {
            date(2021, 1, 11): (2020, 1),
            date(2022, 5, 17): (2021, 5),
            date(2022, 5, 18): (2021, 5),
        }

        extra_months_to_query = set()

        for irregular_gazette_date, year_month in irregular_placing_map.items():
            if (
                self.start_date <= irregular_gazette_date
                and irregular_gazette_date <= self.end_date
                and year_month not in requested_year_month
            ):
                self.logger.info(
                    f"As we are querying a custom period, we will also query"
                    f" {year_month[0]}-{year_month[1]:02}"
                    f" which has a gazette from {irregular_gazette_date.isoformat()}"
                )
                extra_months_to_query.add(date(*year_month, 1))

        return extra_months_to_query

    def extract_date_and_extra_text_from_regex(
        self,
        text,
        pattern,
        day_textual_month_year,  # a 3-tuple containing day as int, textual month and year as int
    ):
        textual_date = "{} de {} de {}".format(*day_textual_month_year)
        extracted_datetime = dateparser.parse(textual_date, languages=["pt"])
        if not extracted_datetime:
            self.logger.warning(f"No date could be extracted from '{text}'")
            return None, ""

        gazette_date = extracted_datetime.date()
        extra_text = pattern.sub("", text).strip()
        return gazette_date, extra_text

    def extract_date_from_text(self, text, monthly_date, edition_number):
        for pattern in [
            REGULAR_FULL_NOMINAL_DATE_RE,
            ALTERNATIVE_REGULAR_FULL_NOMINAL_DATE_RE,
        ]:
            if edition_number in ["1873", "2309"]:
                # The edition_number 1873 of 2017-10-02 and
                # he edition_number 2309 of 2019-07-26
                # have entries that match full nominal date regex
                # but their actual dates should be extracted from
                # the day-month pattern
                break

            if match_ := pattern.search(text):
                return self.extract_date_and_extra_text_from_regex(
                    text,
                    pattern,
                    (match_.group(1), match_.group(2), match_.group(3)),
                )

        if match_ := DAY_MONTH_NOMINAL_DATE_RE.search(text):
            return self.extract_date_and_extra_text_from_regex(
                text,
                REGULAR_FULL_NOMINAL_DATE_RE,
                (match_.group(1), match_.group(2), str(monthly_date.year)),
            )

        self.logger.warning(
            f"No date could be extracted from '{text}'"
            f" for edition_number {edition_number}"
            f" in queried period {monthly_date.strftime('%Y-%m')}"
        )
        return None, text

    def triage_data_per_row(self, raw_title, monthly_date):
        """Triage gazette data from a page row.

        It returns a 3-tuple:
            index 0: edition_number as str or None,
            index 1: gazette_date as date or None,
            index 2: extra_text as str
        """

        edition_number_match = EDITION_NUMBER_RE.match(raw_title)
        if not edition_number_match:
            self.logger.warning(
                f"No edition number could be extracted from '{raw_title}'"
                f" in queried period {monthly_date.strftime('%Y-%m')}"
            )
            return None, None, raw_title

        edition_number = edition_number_match.group(1)

        remaining_text = EDITION_NUMBER_RE.sub("", raw_title).strip()
        gazette_date, extra_text = self.extract_date_from_text(
            remaining_text, monthly_date, edition_number
        )

        return edition_number, gazette_date, extra_text

    def prepare_gazettes_queried_for_an_edition_number(
        self,
        monthly_date,
        edition_number,
        date_extra_text_url_data,
    ):
        """Build Gazette data from the data for an edition_number.

        One reason to implement this method by edition_number was that
        there are some rows that don't have a date to extract, but
        there is at least one other line that contains the date information.

        Thus, we gather all the rows in a month and determine if there is
        a single consistent date for the edition_number: if there is no date or
        there are several dates, we discard the data collected from the edition_number.
        """

        dates_from_data = set()
        extra_text_url_data = {}

        for current_date, extra_text_url in date_extra_text_url_data:
            dates_from_data.add(current_date)
            extra_text_url_data |= extra_text_url

        valid_dates = {valid_date for valid_date in dates_from_data if valid_date}
        if len(valid_dates) == 1:
            gazette_date = valid_dates.pop()
            if gazette_date < self.start_date or self.end_date < gazette_date:
                return []
        elif len(valid_dates) > 1:
            self.logger.warning(
                f"Multiple dates collected for edition_number {edition_number}"
                f" in queried period {monthly_date.strftime('%Y-%m')}:"
                f" {sorted([d.isoformat() for d in valid_dates])}"
            )
            return []
        else:
            self.logger.info(
                f"Unable to collect edition_number {edition_number}"
                " due to missing associated date"
                f" in queried period {monthly_date.strftime('%Y-%m')}"
            )
            return []

        sorted_extra_texts = sorted(extra_text_url_data)

        file_urls_by_is_extra_edition = {}

        for extra_text in sorted_extra_texts:
            file_url = extra_text_url_data[extra_text].replace(
                # some URLs seems to have http hardcoded
                # manually replacing http:// to https:// to avoid a 301 redirect
                "http://noticias.sorocaba.sp.gov.br",
                "https://noticias.sorocaba.sp.gov.br",
            )
            is_extra_edition = extra_text != "" and not REGULAR_GAZETTE_PART_RE.search(
                extra_text
            )
            file_urls_by_is_extra_edition.setdefault(is_extra_edition, []).append(
                file_url
            )

        gazettes = []

        sorted_is_extra_edition = sorted(file_urls_by_is_extra_edition)
        for is_extra_edition in sorted_is_extra_edition:
            gazettes.append(
                Gazette(
                    date=current_date,
                    edition_number=str(edition_number),
                    file_urls=file_urls_by_is_extra_edition[is_extra_edition],
                    is_extra_edition=is_extra_edition,
                    power="executive",
                )
            )

        return gazettes

    def prepare_gazettes_queried_from_monthly_date_period(self, monthly_date):
        """Build Gazette data from the data in the queried monthly_date period.

        There are some rows with the same edition_number that are separated from
        each other by other rows with different edition_number values, so we collect
        all data from a monthly_date period and then handle the data by edition_number.
        """

        data_by_edition_number = self.data_by_monthly_date_by_edition_number.get(
            monthly_date
        )

        if not data_by_edition_number:
            self.logger.info(
                f"No gazette was collected in queried period"
                f" {monthly_date.strftime('%Y-%m')}"
            )
            return []

        gazettes = []

        for edition_number, date_extra_text_url_data in data_by_edition_number.items():
            gazettes.extend(
                self.prepare_gazettes_queried_for_an_edition_number(
                    monthly_date,
                    edition_number,
                    date_extra_text_url_data,
                )
            )

        return gazettes

    def is_row_data_in_manual_block_list(
        self, monthly_date, edition_number, extra_text
    ):
        if edition_number in ["1.188"]:
            # The row marked as edition_number 1.188 has wrong data and its file
            # is a duplicate of 1189 of 2006-01-27
            self.logger.info(
                f"Unable to collect edition_number {edition_number}"
                " because it was manually included in a block list"
            )
            return True

        if edition_number in ["1.394", "1.539", "1.564"] and extra_text:
            # The edition_number 1.394 of 2009-11-27 has 4 rows with the same file:
            # one without extra_text and three with extra_text
            # We chose to discard the entries with extra_text
            #
            # The edition_number 1.539 of 2012-07-24 and
            # the edition_number 1.564 of 2012-12-29
            # have 2 rows with the same file each:
            # one without extra_text and another with extra_text
            # We chose to discard the entries with extra_text

            self.logger.info(
                f"Unable to collect edition_number {edition_number}"
                f" with extra_text '{extra_text}'"
                " because it was manually included in a block list"
            )
            return True

        if edition_number == "2796" and monthly_date.timetuple()[:2] == (
            2021,
            7,
        ):
            # The edition_number 2796 of 2021-08-02 appears in both 2021-07
            # and 2021-08 periods
            # We chose to discard the entry from 2021-07 if it is within
            # the requested range
            self.logger.info(
                f"Unable to collect edition_number {edition_number}"
                f" in queried period {monthly_date.strftime('%Y-%m')}"
                " because it was manually included in a block list"
            )
            return True

        if extra_text in [
            # The edition_number 2204 of 2019-02-15 has two rows with
            # "escala profissional" pointing to the same file: one with
            # the "Copia" extra_text and another without it
            # We are discarding the one stating that it is a copy
            "escala profissional – Copia",
            # The edition_number 2399 of 2019-12-06 has two rows with
            # "escala consolidado" pointing to the same file: one with
            # the longer extra_text and another with a shorter extra_text
            # We are discarding the one with the longer prefix
            "ESCALA CONSOLIDADO 2399 – 06 DE DEZEMBRO DE 2019 – ESCALA PROFISSIONAL",
        ]:
            self.logger.info(
                f"Unable to collect edition_number {edition_number}"
                f" with extra_text '{extra_text}'"
                " because it was manually included in a block list"
            )
            return True

        return False

    def triage_data_per_page(self, response, monthly_date, page_number):
        """Triage gazette data from a page row

        Once we finish all the pages from a monthly_date, we collect
        the gazettes by checking the collected edition_number values
        """

        # There may have an inconsistency for the relativedelta handling
        inconsistent_a_month_before_value = monthly_date - relativedelta(months=1)
        if isinstance(inconsistent_a_month_before_value, datetime):
            a_month_before = inconsistent_a_month_before_value.date()
        else:
            a_month_before = inconsistent_a_month_before_value

        inconsistent_more_than_a_month_later_value = monthly_date + relativedelta(
            months=2
        )
        if isinstance(inconsistent_more_than_a_month_later_value, datetime):
            more_than_a_month_later = inconsistent_more_than_a_month_later_value.date()
        else:
            more_than_a_month_later = inconsistent_more_than_a_month_later_value

        gazette_table = response.xpath(
            "//strong[contains(@class,'titulo-jornal')]/ancestor::a"
        )
        gazettes_links = gazette_table.css("a::attr(href)").getall()
        gazettes_raw_title = gazette_table.css("strong.titulo-jornal::text").getall()

        for url, raw_title in zip(gazettes_links, gazettes_raw_title):
            raw_title = raw_title.strip()
            edition_number, gazette_date, extra_text = self.triage_data_per_row(
                raw_title, monthly_date
            )

            if not edition_number:
                continue

            if self.is_row_data_in_manual_block_list(
                monthly_date, edition_number, extra_text
            ):
                continue

            if (
                gazette_date
                and gazette_date.timetuple()[:2] != monthly_date.timetuple()[:2]
            ):
                if (
                    gazette_date < a_month_before
                    or more_than_a_month_later <= gazette_date
                ):
                    self.logger.warning(
                        f"Data for edition_number {edition_number} with date"
                        f" {gazette_date.isoformat()} was found"
                        " more than a month displaced from"
                        f" the queried period {monthly_date.strftime('%Y-%m')}"
                    )
                else:
                    self.logger.warning(
                        f"Gazette data was found for {gazette_date.isoformat()}"
                        f" in queried period {monthly_date.strftime('%Y-%m')}"
                    )

            self.data_by_monthly_date_by_edition_number.setdefault(
                monthly_date, {}
            ).setdefault(edition_number, []).append((gazette_date, {extra_text: url}))

        next_page_available = response.xpath(
            "//li[contains(@class,'next') and not(contains(@class,'disabled'))]"
        )

        if next_page_available:
            # Keep triaging data of the requested month
            next_page = page_number + 1
            next_url = (
                f"{self.BASE_URL}page/{next_page}/"
                f"?ano={monthly_date.year}%20{MONTH_STR[monthly_date.month]}"
            )
            yield Request(
                response.urljoin(next_url),
                callback=self.triage_data_per_page,
                cb_kwargs={
                    "monthly_date": monthly_date,
                    "page_number": page_number + 1,
                },
            )
        else:
            yield from self.prepare_gazettes_queried_from_monthly_date_period(
                monthly_date
            )
