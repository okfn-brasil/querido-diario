import scrapy
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class BaseDiarioOficialBRSpider(BaseGazetteSpider):
    allowed_domains = ["diariooficialbr.com.br"]

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "BASE_URL"):
            raise NotConfigured("Please set a value for `BASE_URL`")
        
        super(BaseDiarioOficialBRSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = f"{self.BASE_URL}/pesquisa/search?initDate={self.start_date}&endDate={self.end_date}"
        yield scrapy.Request(url)

    def parse(self, response):
        editions_list = response.xpath('//div[contains(@class, "card-downloads")]')
        for edition in editions_list:
            edition_date_selector = edition.xpath(
                './/div[contains(text(), "Publicado")]/text()'
            ).get()
            edition_date = get_date_from_text(edition_date_selector.split("dia")[-1])

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
