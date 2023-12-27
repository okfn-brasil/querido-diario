import re
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseDiarioOficinalBRSpider(BaseGazetteSpider):
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }

    def start_requests(self):
        url = f"{self.url_base}/pesquisa/search?initDate={self.start_date}&endDate={self.end_date}"
        yield scrapy.Request(url)

    def _translate_month(self, month):
        return {
            "janeiro": "01",
            "fevereiro": "02",
            "março": "03",
            "abril": "04",
            "maio": "05",
            "junho": "06",
            "julho": "07",
            "agosto": "08",
            "setembro": "09",
            "outubro": "10",
            "novembro": "11",
            "dezembro": "12",
        }[month]

    def _get_date_from_parent_edition(self, gazette_text):
        gazette_text = gazette_text.lower().replace("1º", "01")
        pattern = r"([1-9]|0[1-9]|[12][0-9]|3[01]) de (janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) de ([0-9]{4})"

        match = re.search(pattern, gazette_text)

        if match:
            raw_date = f"{str(match.group(3))}-{self._translate_month(str(match.group(2)))}-{str(match.group(1))}"
            return datetime.strptime(str(raw_date), "%Y-%m-%d").date()

    def _get_edition_from_name(self, gazette_name):
        pattern = r"nº\s+(\d+)"

        match = re.search(pattern, gazette_name)

        if match:
            return match.group(1)

    def parse(self, response):
        editions_list = response.xpath(
            '//div[contains(@class, "flex") and contains(@class, "card-downloads")]'
        )
        for edition in editions_list:
            edition_date_selector = edition.xpath(
                './/div[contains(@class, "text-gray-800") and contains(@class, "2xl:text-lg")]'
            )

            edition_date = edition_date_selector.xpath("./text()").extract().pop()
            edition_date = self._get_date_from_parent_edition(
                edition_date.split("dia")[-1]
            )

            edition_number_selector = edition.xpath(
                './/span[contains(@class, "mr-3 ")]'
            )
            edition_number = edition_number_selector.xpath("./text()").extract().pop()
            edition_number = self._get_edition_from_name(edition_number)

            edition_url_selector = edition.xpath('.//a[contains(@class, "w-full")]')
            edition_url = edition_url_selector.css("a::attr(href)").get()

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                file_urls=[edition_url],
                is_extra_edition=False,
                power="executive",
            )
        next_page = response.xpath('//a[@aria-label="pagination.next"]')
        if next_page != [] and next_page:
            next_page_url = next_page.css("a::attr(href)").get()
            yield scrapy.Request(next_page_url)
