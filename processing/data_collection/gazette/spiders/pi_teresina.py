import scrapy
import dateparser

from datetime import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PiTeresina(BaseGazetteSpider):
    TERRITORY_ID = "2211001"
    name = "pi_teresina"
    start_urls = ["http://dom.pmt.pi.gov.br/lista_diario.php"]

    def parse(self, response):
        total_items = int(response.css("#meio > div.texto > span > b::text").get())
        total_pages = self.calculate_number_of_pages(total_items, 10)

        pages_urls = [
            "http://dom.pmt.pi.gov.br/lista_diario.php?pagina={}".format(i)
            for i in range(1, total_pages + 1)
        ]
        for url in pages_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        for entry in response.css("tbody > tr"):
            file_url = entry.css("a::attr(href)").get()

            date_text = entry.css("td:nth-child(2)::text").get()
            date = dateparser.parse(date_text, languages=["pt"]).date()

            yield Gazette(
                date=date,
                file_urls=[file_url],
                territory_id=self.TERRITORY_ID,
                power="executive_legislative",
                scraped_at=datetime.utcnow(),
            )

    def calculate_number_of_pages(self, total_items, items_per_page=10):
        if total_items % items_per_page == 0:
            number_of_pages = total_items // items_per_page
        else:
            number_of_pages = (total_items // items_per_page) + 1
        return number_of_pages
