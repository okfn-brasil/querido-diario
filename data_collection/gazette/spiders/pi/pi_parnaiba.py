from datetime import datetime
from scrapy import Request

from scrapy.http.response.html import HtmlResponse
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PiParnaibaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2207702"

    name = "pi_parnaiba"
    start_urls = ["http://dom.parnaiba.pi.gov.br"]

    def parse_page(self, response: HtmlResponse):
        for entry in response.css('.table-diario tbody > tr'):
            edition, date, filename = entry.xpath('./td/text()').extract()
            is_extra_edition = "extra" in filename.lower()
            yield Gazette(
                date=datetime.strptime(date, "%d-%m-%Y").date(),
                file_urls=entry.xpath('./td/a/@href').extract(),
                edition_number=edition,
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power="executive",
            )

    def parse(self, response: HtmlResponse):
        for url in response.css('.pagination a').extract():
            yield Request(url, callback=self.parse_page)
