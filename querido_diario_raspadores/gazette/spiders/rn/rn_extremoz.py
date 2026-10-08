import datetime as dt
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

MONTHS = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}


class RnExtremozSpider(BaseGazetteSpider):
    """
    Os diários ficam em uma página por ano (a partir de 2014) e as edições de
    2006 a 2013 estão reunidas na página "anos anteriores". Em ambas, os diários
    são listados do mais recente para o mais antigo, com paginação.

    Nas páginas mais antigas, a data exibida em cada item é a data de envio do
    arquivo ao site, e não a da edição. Por isso, a data é extraída do título
    do item (ex. "DOEM nº 0784, 22 de outubro de 2013" ou "30 DEZ 2014") e a
    data exibida só é usada quando o título não traz uma data.
    """

    name = "rn_extremoz"
    TERRITORY_ID = "2403608"
    allowed_domains = ["extremoz.rn.gov.br"]
    start_date = dt.date(2006, 8, 4)

    BASE_URL = "https://extremoz.rn.gov.br/diario-oficial"
    FIRST_YEAR_WITH_OWN_PAGE = 2014

    async def start(self):
        if self.start_date.year < self.FIRST_YEAR_WITH_OWN_PAGE:
            yield scrapy.Request(f"{self.BASE_URL}/diario-oficial-anos-anteriores/")

        first_year = max(self.start_date.year, self.FIRST_YEAR_WITH_OWN_PAGE)
        for year in range(first_year, self.end_date.year + 1):
            yield scrapy.Request(f"{self.BASE_URL}/diario-oficial-{year}/")

    def parse(self, response):
        page_dates = []

        for item in response.css("article.arq-list-item"):
            title = " ".join(item.css("h1::text").getall()).strip()
            gazette_date = self.parse_date(title) or self.parse_listed_date(item)
            if gazette_date is None:
                self.logger.warning(f"Data não encontrada para {title!r}")
                continue
            page_dates.append(gazette_date)

            file_url = item.css(".arq-list-item-content a::attr(href)").get()
            # Alguns itens antigos não têm arquivo ou apontam para um PDF
            # genérico de "edição não encontrada"
            if not file_url or "nao-encontrada" in file_url.lower():
                continue

            if not self.start_date <= gazette_date <= self.end_date:
                continue

            edition_number = re.search(r"n[º°o]\.?\s*(\d+)", title, re.IGNORECASE)

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number.group(1) if edition_number else "",
                file_urls=[response.urljoin(file_url)],
                is_extra_edition=bool(
                    re.search(r"extra|especial|suplement", title, re.IGNORECASE)
                ),
                power="executive_legislative",
            )

        # Como a listagem é decrescente, as próximas páginas só têm edições
        # anteriores à mais antiga desta página
        next_page_url = response.css("a.next.page-numbers::attr(href)").get()
        if next_page_url and (not page_dates or min(page_dates) >= self.start_date):
            # Os links de paginação vêm sem a barra final e o site responde
            # com um redirecionamento (301) para a URL com barra
            yield scrapy.Request(response.urljoin(f"{next_page_url.rstrip('/')}/"))

    def parse_date(self, text):
        match = re.search(
            r"(\d{1,2})\s*(?:de\s+)?([a-zç]{3,})\.?\s*(?:de\s+)?(\d{4})",
            text,
            re.IGNORECASE,
        )
        if not match:
            return None

        day, month_name, year = match.groups()
        month = MONTHS.get(month_name[:3].lower())
        if month is None:
            return None

        try:
            return dt.date(int(year), month, int(day))
        except ValueError:
            return None

    def parse_listed_date(self, item):
        raw_date = "".join(item.css("p.data::text").getall()).strip()
        try:
            return dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
        except ValueError:
            return None
