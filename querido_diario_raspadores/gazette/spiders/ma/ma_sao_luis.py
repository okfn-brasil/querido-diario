import datetime as dt
import re

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MASaoLuisSpider(BaseGazetteSpider):
    name = "ma_sao_luis"
    TERRITORY_ID = "2111300"
    allowed_domains = ["diariooficial.saoluis.ma.gov.br"]
    start_date = dt.date(1980, 5, 9)
    power = "executive_legislative"

    archive_url = "https://diariooficial.saoluis.ma.gov.br/api/portal/editions/archive"
    page_size = 200

    async def start(self):
        yield self._archive_request(page=1)

    def _archive_request(self, page):
        return scrapy.Request(
            f"{self.archive_url}?page={page}&limit={self.page_size}",
            cb_kwargs={"page": page},
        )

    def parse(self, response, page):
        data = response.json()
        editions = data.get("editions", [])

        for edition in editions:
            edition_date = dt.date.fromisoformat(edition["edition_date"][:10])
            if not self.start_date <= edition_date <= self.end_date:
                continue

            name = edition.get("edition_number") or edition.get("nome") or ""
            yield Gazette(
                date=edition_date,
                edition_number=self._edition_number(name),
                is_extra_edition=self._is_extra_edition(name),
                file_urls=[response.urljoin(edition["pdf_download_url"])],
                power=self.power,
            )

        # The archive is sorted from the newest to the oldest edition
        if not editions or page >= data.get("total_pages", page):
            return
        oldest_date = dt.date.fromisoformat(editions[-1]["edition_date"][:10])
        if oldest_date >= self.start_date:
            yield self._archive_request(page=page + 1)

    # Edition names found in the archive:
    # "Edição nº 238/XLVI", "diario_oficial_038_XLVI.pdf",
    # "dom-prefeitura-municipal-de-sao-luis-ano-xliv-edicao-0597-assinado.pdf",
    # "DOM-2015-142-S-A123.pdf" (S = supplement) and "DIÁRIO OFICIAL - Nº 19 - 1981.pdf"
    EDITION_NUMBER_PATTERNS = [
        re.compile(r"DOM-\d{4}-(\d+)-"),
        re.compile(r"(\d+)\s*/"),
        re.compile(r"_(\d+)_[IVXLC]+\b"),
        re.compile(r"edicao-(\d+)", re.IGNORECASE),
        re.compile(r"N[º°\W]{0,3}(\d+)", re.IGNORECASE),
    ]

    @classmethod
    def _edition_number(cls, name):
        for pattern in cls.EDITION_NUMBER_PATTERNS:
            match = pattern.search(name)
            if match:
                return str(int(match.group(1)))
        return ""

    @staticmethod
    def _is_extra_edition(name):
        return "extra" in name.lower() or bool(re.search(r"DOM-\d{4}-\d+-S-", name))
