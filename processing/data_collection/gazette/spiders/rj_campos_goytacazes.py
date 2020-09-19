import re
import dateparser

from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjCampoGoytacazesSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301009"

    allowed_domains = ["www.campos.rj.gov.br"]
    name = "rj_campos_goytacazes"
    start_urls = [
        "https://www.campos.rj.gov.br/diario-oficial.php?PGpagina=1&PGporPagina=15"
    ]
    LIMIT_DATE = dateparser.parse("2015-01-01").date()

    def parse(self, response):
        """
        @url https://www.campos.rj.gov.br/diario-oficial.php?PGpagina=1&PGporPagina=15
        @returns requests 1
        @returns items 15 15
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """

        for element in response.css("ul.ul-licitacoes li"):
            gazette_text = element.css("h4::text").extract_first() or ""

            date_re = re.search(r"(\d{2} de (.*) de \d{4})", gazette_text)
            if not date_re:
                continue

            # The extra edition for August 28th, 2018 has a typo in the month name.
            date = date_re.group(0).replace("Agosoto", "Agosto")
            date = dateparser.parse(date, languages=["pt"]).date()

            if date < self.LIMIT_DATE:
                raise CloseSpider("Went further than 2015")

            url = element.css("a::attr(href)").extract_first().strip()
            # From November 17th, 2017 and backwards the path to the gazette PDF
            # is relative.
            if url.startswith("up/diario_oficial.php"):
                url = "https://www.campos.rj.gov.br/%s" % url

            is_extra_edition = gazette_text.startswith("Suplemento")

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
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
            yield Request(response.urljoin(next_url))
