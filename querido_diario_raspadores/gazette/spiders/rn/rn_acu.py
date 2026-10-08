import datetime as dt
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

MONTHS = {
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "marco": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}


class RnAcuSpider(BaseGazetteSpider):
    """
    Assú (grafado "Açu" na tabela do IBGE) publica o seu Diário Oficial no site
    da prefeitura, em uma listagem do mais recente para o mais antigo, com
    25 edições por página. Os arquivos ficam hospedados no Google Drive.

    A coluna de data da listagem é preenchida manualmente e tem alguns erros
    (ex. edição nº 2099, de 08/01/2013, aparece como 18/09/2013), por isso a
    data é extraída preferencialmente do título da edição.
    """

    name = "rn_acu"
    TERRITORY_ID = "2400208"
    allowed_domains = [
        "assu.rn.gov.br",
        "drive.google.com",
        "drive.usercontent.google.com",
    ]
    start_date = dt.date(2013, 1, 2)

    BASE_URL = "https://assu.rn.gov.br/diario_oficial/"

    async def start(self):
        yield scrapy.Request(self.BASE_URL)

    def parse(self, response, page=1):
        page_dates = []

        for item in response.css("#busca_dom .jet-listing-grid__item"):
            fields = [
                text.strip()
                for text in item.css(
                    ".jet-listing-dynamic-field__content ::text"
                ).getall()
                if text.strip()
            ]
            if len(fields) < 3:
                continue
            _, title, raw_date = fields[:3]

            gazette_date = self.parse_date(title) or self.parse_listed_date(raw_date)
            if gazette_date is None:
                self.logger.warning(f"Data não encontrada para {title!r}")
                continue
            page_dates.append(gazette_date)

            if not self.start_date <= gazette_date <= self.end_date:
                continue

            file_id = re.search(
                r"(?:/d/|[?&]id=)([\w-]+)", item.css("a::attr(href)").get(default="")
            )
            if file_id is None:
                self.logger.warning(f"Arquivo não encontrado para {title!r}")
                continue

            edition_number = re.search(r"N[º°o]\.?\s*(\d+)", title, re.IGNORECASE)

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number.group(1) if edition_number else "",
                # O link de visualização do Google Drive abre uma página HTML;
                # este é o link de download direto do arquivo
                file_urls=[
                    f"https://drive.google.com/uc?export=download&id={file_id.group(1)}"
                ],
                is_extra_edition=bool(
                    re.search(r"extra|suplement|especial", title, re.IGNORECASE)
                ),
                power="executive_legislative",
            )

        # Como a listagem é decrescente, as próximas páginas só têm edições
        # anteriores à mais antiga desta página
        listing = response.css("#busca_dom .jet-listing-grid__items")
        last_page = int(listing.attrib.get("data-pages", page))
        if page < last_page and (not page_dates or min(page_dates) >= self.start_date):
            yield scrapy.Request(
                f"{self.BASE_URL}?jsf=jet-engine:busca_dom&pagenum={page + 1}",
                cb_kwargs={"page": page + 1},
            )

    def parse_date(self, title):
        match = re.search(r"(\d{1,2})\s+de\s+([a-zç]+)\s+de\s+(\d{4})", title, re.I)
        if not match:
            return None

        day, month_name, year = match.groups()
        month = MONTHS.get(month_name.lower())
        if month is None:
            return None

        try:
            return dt.date(int(year), month, int(day))
        except ValueError:
            return None

    def parse_listed_date(self, raw_date):
        try:
            return dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
        except ValueError:
            return None
