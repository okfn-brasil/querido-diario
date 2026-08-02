import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnMossoroSpider(BaseGazetteSpider):
    TERRITORY_ID = "2408003"
    name = "rn_mossoro_2023"
    start_date = dt.date(2023, 1, 2)
    allowed_domains = ["dom.mossoro.rn.gov.br"]
    start_urls = ["https://dom.mossoro.rn.gov.br/dom/edicoes"]

    def parse(self, response):
        for edition in response.css("div.edicoes-list div.col-md-3"):
            raw_date = edition.css("div.card-content p::text").get().strip()
            gazette_date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()

            if gazette_date > self.end_date:
                continue
            if self.start_date > gazette_date:
                return

            intermediary_page = edition.css("a::attr(href)").get()
            yield scrapy.Request(
                response.urljoin(intermediary_page),
                callback=self.parse_gazette_page,
                cb_kwargs={"gazette_date": gazette_date},
            )

        next_page_url = response.xpath(
            "//a[contains(text(), 'PRÓXIMA PÁGINA')]/@href"
        ).get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def extra_edition_check(self, edition_number):
        if edition_number.isdigit():
            return False
        return True

    def parse_gazette_page(self, response, gazette_date):
        edition_number = response.xpath(
            "//div[@id='main-content']//li[3]//strong/text()"
        ).get()
        file_link = response.xpath(
            "//div[@id='main-content']//a[contains(@href, '/pmm/uploads/publicacao/pdf')]/@href"
        ).get()

        yield Gazette(
            date=gazette_date,
            edition_number=edition_number,
            file_urls=[response.urljoin(file_link)],
            is_extra_edition=self.extra_edition_check(edition_number),
            power="executive",
        )
