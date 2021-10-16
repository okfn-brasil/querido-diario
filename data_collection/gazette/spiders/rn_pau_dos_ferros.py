import datetime

from dateparser import parse
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RnPauDosFerrosSpider(BaseGazetteSpider):
    name = "rn_pau_dos_ferros"
    allowed_domains = ["paudosferros.rn.gov.br"]
    start_date = datetime.date(2017, 1, 2)
    TERRITORY_ID = "2409407"
    start_urls = ["https://paudosferros.rn.gov.br/publicacoes.php"]

    def parse(self, response):
        gazettes = response.css(".list-group-item")
        last_page_number_css = ".pagination > li:nth-last-child(-n+2) > a > span::text"
        last_page_number = int(response.css(last_page_number_css).extract_first())
        follow_next_page = True

        for gazette in gazettes:
            gazette_date_raw = (
                gazette.css("div > div > span::text").extract_first().strip()
            )
            gazette_date = parse(gazette_date_raw, languages=["pt"]).date()

            gazette_partial_name = "DIARIO OFICIAL:"
            gazette_title_raw = gazette.css(
                "h4 > div > div > strong::text"
            ).extract_first()
            is_extra_edition = not (gazette_partial_name in gazette_title_raw)
            edition_number = (
                None
                if is_extra_edition
                else gazette_title_raw.replace(gazette_partial_name, "").strip()
            )

            if gazette_date < self.start_date:
                follow_next_page = False
                break

            partial_url = gazette.css("a::attr(href)").extract_first()
            url = f"https://paudosferros.rn.gov.br/{partial_url}"

            yield Gazette(
                date=gazette_date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                edition_number=edition_number,
                power="executive_legislative",
            )

        if follow_next_page:
            for page in range(1, last_page_number):
                yield Request(
                    f"https://paudosferros.rn.gov.br/publicacoes.php?pagina={page}",
                )
