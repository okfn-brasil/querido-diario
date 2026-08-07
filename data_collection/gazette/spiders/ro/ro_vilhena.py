import re
from datetime import date

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

GAZETTE_YEAR_PATTERN = re.compile(r"DOV's do Ano de ([0-9]{4})")
GAZETTE_MONTH_YEAR_PATTERN = re.compile(r"DOV's.*\(([0-9]{2})/([0-9]{4})\)")
GAZETTE_TEXT_PATTERN = re.compile(
    r"DOV N[^0-9]+"
    r"([0-9]+)(?# edition_number)"
    r"[^0-9]+"
    r"([0-9]{2})(?# gazette day)"
    r"."
    r"([0-9]{2})(?# gazette month)"
    r"."
    r"([0-9]{4})(?# gazette year)"
    r"\s*"
    r"(\S*)(?# possible suffix)"
)


class RoVilhena(BaseGazetteSpider):
    name = "ro_vilhena"
    TERRITORY_ID = "1100304"
    start_date = date(2017, 3, 7)  # edition_number 2189

    BASE_URL = "http://dov.vilhena.ro.gov.br/"
    allowed_domains = [
        "dov.vilhena.ro.gov.br",
        "vilhenaro.wixsite.com",
        "vilhena.xyz",
    ]

    def __init__(self, *args, **kwargs):
        super(RoVilhena, self).__init__(*args, **kwargs)

        # During the development of this spider, we found out that some entries were duplicated
        # We use a set with a 3-tuple composed by
        #     - gazette_date
        #     - edition_number
        #     - url
        # to store the entry uniqueness before continuing its processing.
        self.found_gazette_data = set()

    def start_requests(self):
        yield Request(
            url="https://vilhenaro.wixsite.com/vilhena-pmv/diario",
            headers={
                "Referer": self.BASE_URL,
            },
            callback=self.initial_parse,
        )

    def initial_parse(self, response):
        today = date.today()
        current_year = today.year
        current_month = today.month

        # Retrieve past years data from page
        past_years_xpath = '//span[starts-with(text(), "DOV\'s do Ano de ")]'
        available_past_years = {}

        for year_node in response.xpath(past_years_xpath):
            node_text = year_node.xpath("./text()").get().strip()

            match_ = GAZETTE_YEAR_PATTERN.search(node_text)
            if not match_:
                self.logger.info(f"Unable to extract year data from '{node_text}'")
                continue

            year_value = int(match_.group(1))
            url = year_node.xpath("./ancestor::a/@href").get().strip()

            if not url:
                self.logger.info(f"No URL could be extracted for year {year_value}")
                continue

            available_past_years[year_value] = url

        for iterable_year in available_past_years:
            if (
                iterable_year < self.start_date.year
                or self.end_date.year < iterable_year
            ):
                continue

            yield Request(
                available_past_years[iterable_year],
                callback=self.parse_year,
                cb_kwargs={"year": iterable_year, "month": 12},
                # Whenever we request a past year, it sets the month to December
            )

        yield from self.parse_year(response, current_year, current_month)

    def parse_year(self, response, year, month):
        # Retrieve past months data from page
        past_months_xpath = f"//span[contains(text(), '/{year})')]"
        available_past_months = {}

        for month_node in response.xpath(past_months_xpath):
            node_text = month_node.xpath("./text()").get().strip()

            match_ = GAZETTE_MONTH_YEAR_PATTERN.search(node_text)
            if not match_:
                self.logger.info(f"Unable to extract month data from '{node_text}'")
                continue

            month_value = int(match_.group(1))
            year_value = int(match_.group(2))
            if year_value != year:
                self.logger.info(
                    f"An unexpected data for year {year} was found: '{node_text}'"
                )
                continue

            url = month_node.xpath("./ancestor::a/@href").get().strip()
            if not url:
                self.logger.info(
                    f"No URL could be extracted for {year_value}-{month_value:02d}"
                )
                continue

            available_past_months[month_value] = url

        first_day_of_start_date_month = date(
            self.start_date.year, self.start_date.month, 1
        )

        for iterable_month in available_past_months:
            first_day_of_month = date(year, iterable_month, 1)
            if (
                first_day_of_month < first_day_of_start_date_month
                or self.end_date < first_day_of_month
            ):
                continue

            yield Request(
                available_past_months[iterable_month],
                callback=self.parse_month,
                cb_kwargs={"year": year, "month": iterable_month},
            )

        first_day_of_month = date(year, month, 1)
        if (
            first_day_of_month < first_day_of_start_date_month
            or self.end_date < first_day_of_month
        ):
            return

        yield from self.parse_month(response, year, month)

    def parse_month(self, response, year, month):
        gazette_text_xpath = "//h2[contains(descendant-or-self::*/text(), 'DOV N')]"

        direct_gazette_url_xpath = ".//a/@href"
        indirect_gazette_url_xpath = (
            "./ancestor::div[@data-testid='richTextElement']"
            "/preceding-sibling::div[descendant::a[@data-testid='linkElement']]"
            "//a[@data-testid='linkElement']"
            "/@href"
        )

        for gazette_text_node in response.xpath(gazette_text_xpath):
            node_text = (
                gazette_text_node.xpath(
                    "descendant-or-self::*[contains(text(), 'DOV N')]/text()"
                )
                .get()
                .strip()
            )

            match_ = GAZETTE_TEXT_PATTERN.search(node_text)
            if not match_:
                self.logger.info(f"Unable to extract gazette data from '{node_text}'")
                continue

            edition_number = match_.group(1)
            day_value = int(match_.group(2))
            month_value = int(match_.group(3))
            year_value = int(match_.group(4))
            suffix_value = match_.group(5)

            if year_value != year:
                self.logger.info(
                    f"An unexpected data for year {year} was found: '{node_text}'"
                )
                continue
            if month_value != month:
                self.logger.info(
                    f"An unexpected data for month {month} was found: '{node_text}'"
                )
                continue

            gazette_date = date(year_value, month_value, day_value)

            if gazette_date < self.start_date or self.end_date < gazette_date:
                continue

            url_data_node = gazette_text_node.xpath(direct_gazette_url_xpath)
            if not url_data_node:
                url_data_node = gazette_text_node.xpath(indirect_gazette_url_xpath)
                if not url_data_node:
                    self.logger.info(
                        f"No URL could be extracted for {gazette_date.isoformat()}"
                    )
                    continue

            url = (
                url_data_node.get().strip()
                # At some point, the domain vilhena.hol.es was replaced with vilhena.xyz
                # but the links weren't updated
                .replace("vilhena.hol.es", "vilhena.xyz")
                # 2018-09-13 has wrong domain
                .replace("vilhenaro.xyz", "vilhena.xyz")
                # vilhena.xyz has https://, but some links point to hardcoded http://
                .replace("http://vilhena.xyz", "https://vilhena.xyz")
            )

            gazette_tuple = (gazette_date, edition_number, url)

            if gazette_tuple in self.found_gazette_data:
                self.logger.info(
                    f"A previous entry for edition_number {edition_number}"
                    f" for {gazette_date.isoformat()} and same URL was registered."
                    f" Skipping..."
                )
                continue

            self.found_gazette_data.add(gazette_tuple)

            yield Gazette(
                edition_number=edition_number,
                date=gazette_date,
                is_extra_edition=bool(suffix_value),
                file_urls=[url],
                power="executive",
            )
