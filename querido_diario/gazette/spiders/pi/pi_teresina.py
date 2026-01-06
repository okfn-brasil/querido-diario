import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PiTeresina(BaseGazetteSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2211001"
    name = "pi_teresina"
    allowed_domains = ["dom.pmt.pi.gov.br"]
    start_date = datetime.date(2005, 1, 7)

    def start_requests(self):
        initial_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")

        url_params = f"pagina=1&filtra_data={initial_date}&filtra_dataf={end_date}"
        yield scrapy.Request(
            f"https://dom.pmt.pi.gov.br/lista_diario.php?{url_params}",
        )

    def parse(self, response):
        for entry in response.css("tbody tr"):
            edition_number = entry.xpath(".//td[1]/text()").get()
            gazette_date = entry.xpath(".//td[2]/text()").get()
            gazette_date = datetime.datetime.strptime(gazette_date, "%d/%m/%Y").date()
            gazettes_pdfs = entry.css("a::attr(href)").getall()

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=gazettes_pdfs,
                is_extra_edition=False,
                power="executive",
            )

        for next_page_url in response.css("a.paginacao::attr(href)").getall():
            yield scrapy.Request(response.urljoin(next_page_url))
