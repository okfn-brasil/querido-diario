import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseDiarioOficialBRSpider(BaseGazetteSpider):
    def start_requests(self):
        url = f"{self.BASE_URL}/pesquisa/search?initDate={self.start_date}&endDate={self.end_date}"
        yield scrapy.Request(url)

    def parse(self, response):
        editions_list = response.xpath('//div[contains(@class, "card-downloads")]')
        for edition in editions_list:
            edition_date_selector = edition.xpath(
                './/div[contains(text(), "Publicado")]/text()'
            ).get()
            edition_date = dateparser.parse(
                edition_date_selector.split("dia")[-1], languages=["pt"]
            ).date()

            edition_number_raw = edition.xpath(
                './/span[contains(text(), "Edição")]/text()'
            )
            edition_number = edition_number_raw.re_first("nº\s+(\d+)")
            is_extra_edition = "extra" in edition_number_raw.get().lower()
            edition_url = edition.xpath(
                './/a[contains(@href, "/download")]/@href'
            ).get()

            yield Gazette(
                date=edition_date,
                edition_number=edition_number,
                file_urls=[edition_url],
                is_extra_edition=is_extra_edition,
                power="executive",
            )

        next_page_url = response.xpath('//a[@aria-label="pagination.next"]/@href').get()
        if next_page_url:
            yield scrapy.Request(next_page_url)
