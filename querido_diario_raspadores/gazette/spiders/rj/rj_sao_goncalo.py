import re
from datetime import date, datetime
from urllib.parse import urlencode

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjSaoGoncaloSpider(BaseGazetteSpider):
    name = "rj_sao_goncalo"
    TERRITORY_ID = "3304904"
    allowed_domains = ["do.pmsg.rj.gov.br"]
    start_date = date(1998, 2, 3)

    BASE_URL = "https://do.pmsg.rj.gov.br/index"
    TERM_PRESENT_IN_EVERY_EDITION = "a"
    FIRST_NUMBERED_EDITION_DATE = date(2020, 8, 18)
    EDITION_NUMBER_RE = re.compile(r"N\.?\s*[º°]\s*(\d{1,3}(?:\.\s?\d{3})+|\d+)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()

    async def start(self):
        yield Request(self.listing_url(1), cb_kwargs={"page": 1})

    def parse(self, response, page):
        for card in response.xpath("//div[@class='card mb-3']"):
            header = card.xpath("./div[@class='card-header']")
            link = header.xpath(".//a")
            gazette_date = datetime.strptime(
                link.xpath("./text()").get().strip(), "%d/%m/%Y"
            ).date()

            url = self.file_url(response, link.attrib["href"])
            if url in self.seen_urls:
                continue
            self.seen_urls.add(url)

            yield Gazette(
                date=gazette_date,
                edition_number=self.edition_number(card, gazette_date),
                is_extra_edition="EXTRA" in header.get().upper(),
                power="executive",
                file_urls=[url],
            )

        pages = response.xpath("//ul[contains(@class, 'pagination')]//a/@href").re(
            r"NumeroPagina=(\d+)"
        )
        if any(int(p) > page for p in pages):
            yield Request(self.listing_url(page + 1), cb_kwargs={"page": page + 1})

    def edition_number(self, card, gazette_date):
        if gazette_date < self.FIRST_NUMBERED_EDITION_DATE:
            return ""
        body = " ".join(card.xpath("./div[@class='card-body']//text()").getall())
        match = self.EDITION_NUMBER_RE.search(body)
        return re.sub(r"\D", "", match.group(1)) if match else ""

    def file_url(self, response, href):
        return response.urljoin(self.with_four_digit_year(href))

    @staticmethod
    def with_four_digit_year(href):
        return re.sub(r"^diario/(\d{2})_", r"diario/20\1_", href)

    def listing_url(self, page):
        query = urlencode(
            {
                "NumeroPagina": page,
                "Termo": self.TERM_PRESENT_IN_EVERY_EDITION,
                "DataInicial": self.start_date.isoformat(),
                "DataFinal": self.end_date.isoformat(),
                "PesquisarTermo": "Pesquisar",
            }
        )
        return f"{self.BASE_URL}?{query}"
