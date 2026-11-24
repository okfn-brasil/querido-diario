import re
from datetime import date
from string import punctuation

import dateparser
from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

PRE_2013_SPLIT_GAZETTE_TEXT_PATTERN = re.compile(
    r"(\d{1,2}(?# day)"
    r"\s+de\s+"
    rf"[^\d\s{punctuation}]+(?# nominal month in pt)"
    r"\s+de\s+"
    r"\d{4})(?# year)"
    r"\s*[-–]+\s+"
    r"Edição[^0-9]+"
    r"([0-9]+)(?# edition_number)"
    r"\s*[-–]?\s*"
    rf"(\w?.*)(?# non-empty in case is_extra_edition_based_on_its_text)",
    flags=re.IGNORECASE,
)
IS_EXTRA_EDITION_PATTERN = re.compile(
    # sumplemento is a typo found in 2018-05-17
    # suplmento is a typo found in 2018-06-20
    # extraordinária found in 2020-09-05
    r"(sum?ple?mento|extraordinária)",
    flags=re.IGNORECASE,
)


# The parameters the with GazettesDataPerPage inline comment rely on
# a particular nested dict structure to temporarily store all the collected metadata.
#
# That storage is a dict in which the key is a tuple composed by 3 items:
#   - gazette_date
#   - edition_number
#   - is_extra_edition
#
# As there can be multiple files for a single combination, the value of the outer dict is
# another dict this time using the is_extra_edition_text as key and a set of urls
# as the innermost value.
#
# Here are some examples where there are multiple files for the same day
#
# {
#     (date(2010, 4, 15), '813', False): {
#         'Parte 1': {
#             'https://www.domjp.com.br/pdf/2010-04-15-part.1.pdf',
#         },
#         'Parte 2': {
#             'https://www.domjp.com.br/pdf/2010-04-15-part.2.pdf',
#         },
#     },
#
#     (date(2010, 7, 14), '874', False): {
#         '': {
#             'https://www.domjp.com.br/pdf/2010-07-14.pdf',
#         },
#     },
#     (date(2010, 7, 14), '874', True): {
#         'Parte 2': {
#             'https://www.domjp.com.br/pdf/2010-07-14-suplemento.pdf',
#         },
#     },
#
#     (date(2023, 1, 10), '3930', False): {
#         '': {
#             'https://diariooficialjp.com.br/pdf/2023-01-10.pdf',
#         },
#     },
#     (date(2023, 1, 10), '3930', True): {
#         'SUPLEMENTO': {
#             'https://diariooficialjp.com.br/pdf/2023-01-10-suplemento.pdf',
#         },
#     },
# }


class RoJiParana(BaseGazetteSpider):
    name = "ro_ji_parana_2010_2013"
    TERRITORY_ID = "1100122"
    start_date = date(2010, 1, 4)  # edition_number 743
    end_date = date(2013, 5, 31)  # edition_number 1585

    BASE_URL = "https://diariooficialjp.com.br/"
    PRE_2013_SPLIT_MONTHLY_FORMAT = (
        "https://www.diariooficialjp.com.br/diarios/{year}{month}.php"
    )
    BASE_URL_FOR_FILES = "https://www.domjp.com.br"

    allowed_domains = [
        "domjp.com.br",
        "diariooficialjp.com.br",
    ]

    # Given that after reaching a certain rate limit, servers responds with 403,
    # we have adjusted some values to avoid this situation.
    custom_settings = {
        "CONCURRENT_ITEMS": 50,
        "CONCURRENT_REQUESTS": 6,
        "DOWNLOAD_DELAY": 1.5,  # 1500 ms
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def start_requests(self):
        initial_date = date(self.start_date.year, 1, 1)

        for monthly_date in rrule(
            freq=MONTHLY,
            dtstart=initial_date,
            until=self.end_date,
        ):
            year = monthly_date.year
            month = monthly_date.month

            yield Request(
                self.PRE_2013_SPLIT_MONTHLY_FORMAT.format(
                    year=year, month=f"{month:02d}"
                ),
                callback=self.parse_month_pre_2013_split,
                cb_kwargs={"year": year, "month": month},
            )

    def parse_month_pre_2013_split(self, response, year, month):
        current_gazettes_data_per_page = {}

        gazette_data_xpath = (
            "//td[@align='center' and descendant::a["
            f" @href and contains(text(), 'Edição') and contains(text(), ' de {year}')"
            "]]"
            f"//a[@href and contains(text(), 'Edição') and contains(text(), ' de {year}')]"
        )

        for gazette_node in response.xpath(gazette_data_xpath):
            node_text = gazette_node.xpath("./text()").get().strip()

            match_ = PRE_2013_SPLIT_GAZETTE_TEXT_PATTERN.search(node_text)
            if not match_:
                self.logger.info(f"Unable to extract gazette data from '{node_text}'")
                continue

            nominal_date = match_.group(1).strip()
            edition_number = match_.group(2)
            is_extra_edition_text = match_.group(3).strip()

            extracted_datetime = dateparser.parse(nominal_date, languages=["pt"])
            if not extracted_datetime:
                self.logger.error(f"No date could be extracted from '{nominal_date}'")
                continue

            gazette_date = extracted_datetime.date()
            if gazette_date.timetuple()[:2] != (year, month):
                self.logger.warning(
                    f"Extracted date {gazette_date.isoformat()} is not from"
                    f" queried period {year}-{month:02d}."
                    " Skipping..."
                )
                continue

            if not (self.start_date <= gazette_date <= self.end_date):
                continue

            file_url = gazette_node.xpath("./@href").get().strip()
            if "http" in file_url:
                # absolute URL
                url = (
                    file_url
                    # There are a few old hardcoded http:// URLs
                    # By manually replacing it with https://, we avoid a few 302 redirections
                    .replace("http://", "https://")
                )
            else:
                # relative URL
                # we need to change the base URL because the pages were transposed
                # to another domain, but not the files
                url = f"{self.BASE_URL_FOR_FILES}{file_url}"

            is_extra_edition_based_on_its_text = bool(
                IS_EXTRA_EDITION_PATTERN.search(is_extra_edition_text)
            )
            is_extra_edition_based_on_its_url = bool(
                IS_EXTRA_EDITION_PATTERN.search(url)
            )
            is_extra_edition = (
                is_extra_edition_based_on_its_text or is_extra_edition_based_on_its_url
            )

            self._validate_uniqueness(
                current_gazettes_data_per_page,
                gazette_date,
                edition_number,
                is_extra_edition,
                is_extra_edition_text,
                url,
            )

        # After gathering all the data in this page, we will sort the data to
        # retrieve the actual gazettes
        yield from self._yield_gazettes(current_gazettes_data_per_page)

    def _validate_uniqueness(
        self,
        current_gazettes_data_per_page,  # GazettesDataPerPage
        gazette_date,
        edition_number,
        is_extra_edition,
        is_extra_edition_text,
        url,
    ):
        current_gazette_key = (
            gazette_date,
            edition_number,
            is_extra_edition,
        )
        current_gazette_url_set = current_gazettes_data_per_page.setdefault(
            current_gazette_key, {}
        ).setdefault(is_extra_edition_text, set())

        if url in current_gazette_url_set:
            self.logger.info(
                f"A previous entry for edition_number {edition_number}"
                f" for {gazette_date.isoformat()}, same is_extra_edition value"
                f" and same URL was registered. Skipping..."
            )
            return

        current_gazette_url_set.add(url)

    def _yield_gazettes(
        self,
        current_gazettes_data_per_page,  # GazettesDataPerPage
    ):
        for (
            gazette_date,
            edition_number,
            is_extra_edition,
        ), by_is_extra_edition_text in current_gazettes_data_per_page.items():
            # Sort urls by is_extra_edition_text
            yield_gazette = True
            current_gazette_urls = []
            for key in sorted(by_is_extra_edition_text):
                url_set = by_is_extra_edition_text[key]
                if len(url_set) > 1:
                    self.logger.error(
                        f"More than one URL was found"
                        f" for edition_number {edition_number}"
                        f" for {gazette_date.isoformat()}, and"
                        f" same is_extra_edition value."
                    )
                    yield_gazette = False
                else:
                    url = url_set.pop()
                    current_gazette_urls.append(url)

            if not yield_gazette:
                continue

            yield Gazette(
                edition_number=edition_number,
                date=gazette_date,
                is_extra_edition=is_extra_edition,
                file_urls=current_gazette_urls,
                power="executive",
            )
