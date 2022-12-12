import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RsCaxiasDoSulSpider(BaseGazetteSpider):
    TERRITORY_ID = "4305108"
    name = "rs_caxias_do_sul"
    allowed_domains = ["caxias.rs.gov.br"]
    start_date = datetime.date(2015, 1, 1)

    def start_requests(self):
        start_date = self.start_date.strftime("%d-%m-%y")
        end_date = self.end_date.strftime("%d-%m-%y")

        start_url = (
            "https://doe.caxias.rs.gov.br/site/index"
            "?PublicacoesSearch[dt_publicacao]="
            f"&PublicacoesSearch[dt_range]={start_date}+até+{end_date}"
            "&PublicacoesSearch[palavra_chave]="
            "&PublicacoesSearch[num_publicacao]="
            "&page=1"
        )
        yield scrapy.Request(start_url)

    def parse(self, response):
        for gazette in response.css(".table tbody tr"):
            edition_number = gazette.xpath("./td[1]/text()").get()
            raw_gazette_date = gazette.xpath("./td[2]/text()").get().strip()
            gazette_date = datetime.datetime.strptime(
                raw_gazette_date, "%d/%m/%Y"
            ).date()
            is_extra_edition = gazette.xpath("./td[3]/text()").get() != "Normal"

            gazette_url = response.urljoin(
                gazette.xpath(".//a[contains(@title, 'Baixar')]/@href").get()
            )
            yield Gazette(
                date=gazette_date,
                file_urls=[
                    gazette_url,
                ],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive",
            )

        next_page_url = response.css(".pagination .next a::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url))
