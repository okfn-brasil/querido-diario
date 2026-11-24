from datetime import date, datetime

from scrapy import Request, Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AlCoruripeSpider(BaseGazetteSpider):
    name = "al_coruripe"
    TERRITORY_ID = ""
    allowed_domains = ["diario.coruripe.al.gov.br"]
    start_urls = ["https://diario.coruripe.al.gov.br"]
    start_date = date(2021, 12, 3)
    BASE_URL = "https://diario.coruripe.al.gov.br"
    is_extra_list = []

    def start_requests(self):
        url = f"{self.BASE_URL}/busca?term=&onde=tudo&data=qualquer&jornal=extra"
        yield Request(url=url, method="GET", callback=self.parse)

    def parse(self, response):
        items = response.css(".accordion-item").getall()
        for item in items:
            item_selector = Selector(text=item)
            self.is_extra_list.append(
                item_selector.xpath(
                    '//button[@class="accordion-button"]/text()'
                ).re_first(r"nº\r\n\s*(\d+)")
            )

        url = f"{self.BASE_URL}/busca?term=&onde=tudo&data=qualquer&jornal=tudo"
        yield Request(url=url, method="GET", callback=self._get_all_gazette)

    def _get_all_gazette(self, response):
        items = response.css(".accordion-item").getall()
        for item in items:
            item_selector = Selector(text=item)
            date_str = item_selector.xpath(
                '//div[@class="me-auto p-2 bd-highlight"]/text()'
            ).re_first(r"\d{2}\/\d{2}\/\d{4}")
            date = datetime.strptime(date_str, "%d/%m/%Y").date()
            file_urls = [item_selector.xpath("//a/@href").get()]
            edition_number = item_selector.xpath(
                '//button[@class="accordion-button"]/text()'
            ).re_first(r"nº\r\n\s*(\d+)")
            scraped_at = datetime.now()
            yield Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=edition_number in self.is_extra_list,
                file_urls=file_urls,
                power="executive",
                scraped_at=scraped_at,
                territory_id="2702306",
            )
