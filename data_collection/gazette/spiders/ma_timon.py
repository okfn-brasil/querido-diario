from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaTimonSpider(BaseGazetteSpider):
    TERRITORY_ID = "2112209"
    name = "ma_timon"
    BASE_URL = "https://timon.ma.gov.br/semgov/diario/"
    allowed_domains = ["timon.ma.gov.br"]
    start_urls = ["https://timon.ma.gov.br/semgov/diario/listagem.php"]

    start_date = date(2013, 3, 20)

    def get_pages(self, response):
        pages = response.css(".pagination-large a ::attr(href)").getall()
        pages.remove("listagem?pagina=0")  # remove link broken
        return pages

    def parse(self, response):
        pages = self.get_pages(response)

        for page in pages:
            url = f"{self.BASE_URL}/{page}"
            yield scrapy.Request(url)

            gazettes = response.css(".arquivos tr:nth-child(1)")

            for gazette in gazettes:
                title = gazette.css(".text-left ::text").get().replace("\xa0", "")
                url = f"{self.BASE_URL}{gazette.css('.text-center ::attr(href)')[1].get()}.pdf"
                str_date = gazette.css(".text-center ::text")[1].get().replace("\t", "")
                date = datetime.strptime(str_date, "%d/%m/%Y").date()

                if self.start_date <= date <= self.end_date:
                    yield Gazette(
                        edition_number=title,
                        date=date,
                        file_urls=[url],
                        is_extra_edition="sup" in title.lower(),
                        territory_id=self.TERRITORY_ID,
                        power="executive",
                    )
