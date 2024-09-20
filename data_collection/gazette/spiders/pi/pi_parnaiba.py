from datetime import date, datetime

from scrapy import Request
from scrapy.http.response.html import HtmlResponse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PiParnaibaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2207702"

    name = "pi_parnaiba"
    allowed_domains = ["dom.parnaiba.pi.gov.br"]
    start_urls = ["http://dom.parnaiba.pi.gov.br/"]
    start_date = date(2017, 8, 1)

    def parse_page(self, response: HtmlResponse):
        for entry in response.css(".table-diario tbody > tr"):
            edition, gazzete_date, filename = entry.xpath("./td/text()").extract()
            gazzete_date = datetime.strptime(gazzete_date, "%d-%m-%Y").date()

            if not self.start_date <= gazzete_date <= self.end_date:
                continue

            file_path = entry.xpath("./td/a/@href").extract_first()
            is_extra_edition = "extra" in filename.lower()
            yield Gazette(
                date=gazzete_date,
                file_urls=[self.start_urls[0] + file_path],
                edition_number=edition,
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power="executive",
            )

    def parse(self, response: HtmlResponse):
        pages_urls = response.xpath("//ul[@class='pagination']//a/@href")
        for url in pages_urls.extract():
            yield Request(url, callback=self.parse_page)
