import re
from datetime import date, datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjParatySpider(BaseGazetteSpider):
    name = "rj_paraty"
    TERRITORY_ID = "3303807"
    allowed_domains = ["paraty.rj.gov.br"]
    start_date = date(2017, 9, 1)
    BASE_URL = "https://www.paraty.rj.gov.br/API/API/Documentos?PageSize=100"

    def start_requests(self):
        yield scrapy.Request(
            url=f"{self.BASE_URL}&PageNumber=1",
            headers={"Accept": "application/json"},
            meta={"page": 1},
        )

    def parse(self, response):
        data = response.json()
        if not data:
            return

        for doc in data:
            gazette_date_str = doc["DataPublicacao"]
            try:
                gazette_date = dt.strptime(gazette_date_str, "%d/%m/%Y").date()
            except ValueError:
                continue

            if gazette_date > self.end_date:
                continue

            if gazette_date < self.start_date:
                return

            doc_file_info = doc["DocumentoArquivoAtual"]
            if not doc_file_info:
                continue

            file_url = doc_file_info["CaminhoLogicoArquivo"]

            title = doc["Titulo"].strip()
            cleaned_text = re.sub(r"[^\d/]", "", title)
            match = re.search(r"(\d+)/\d{4}", cleaned_text)
            edition_number = match.group(1) if match else None

            is_extra = "EXTRA" in title.upper()
            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra,
                file_urls=[file_url],
                power="executive_legislative",
            )
        page = response.request.meta["page"] + 1
        yield scrapy.Request(
            url=f"{self.BASE_URL}&PageNumber={page}",
            headers={"Accept": "application/json"},
            meta={"page": page},
        )
