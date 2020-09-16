import re
import dateparser

from datetime import datetime
from scrapy import Request
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjCampoGoytacazesSpider(BaseGazetteSpider):
    GAZETTE_ELEMENT_CSS = "ul.ul-licitacoes li"
    TERRITORY_ID = "3301009"

    allowed_domains = ["www.campos.rj.gov.br"]
    name = "rj_campos_goytacazes"
    start_urls = [
        "https://www.campos.rj.gov.br/diario-oficial.php?PGpagina=1&PGporPagina=15"
    ]

    def parse(self, response):
        """
        @url https://www.campos.rj.gov.br/diario-oficial.php?PGpagina=1&PGporPagina=15
        @returns requests 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css(self.GAZETTE_ELEMENT_CSS):
            url = element.css("a::attr(href)").extract_first()
            gazette_text = element.css("h4::text").extract_first()
            extra_edition = gazette_text.startswith("Suplemento")

            date_re = re.search(r"(\d{2} de (.*) de \d{4})", gazette_text)
            if date_re:
                date = dateparser.parse(date_re.group(0), languages=["pt"]).date()

                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=extra_edition,
                    territory_id=self.TERRITORY_ID,
                    power="executive",
                    scraped_at=datetime.utcnow(),
                )

        next_url = (
            response.css(".pagination")
            .xpath("//a[contains(text(), 'Proxima')]/@href")
            .extract_first()
        )
        if next_url:
            print(next_url)
            yield Request(response.urljoin(next_url))
