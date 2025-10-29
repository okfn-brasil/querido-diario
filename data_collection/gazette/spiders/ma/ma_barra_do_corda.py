import datetime
import json

from scrapy import Request, exceptions

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MABarraDoCordaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2101608"
    name = "ma_barra_do_corda"
    allowed_domains = ["dom.barradocorda.ma.gov.br"]

    BASE_API_URL = "https://dom.barradocorda.ma.gov.br/api/v1/diary/editions"
    BASE_PDF_URL = "https://dom.barradocorda.ma.gov.br/uploads/editions/13/"

    start_date = datetime.date(2022, 1, 10)

    static_body_payload = json.dumps(
        {
            "slug": "dom.barradocorda.ma.gov.br",
            "dates": "",
            "term": "",
            "type_publication": "",
            "type_book": "",
            "number_edition": "",
            "limit": "10",
        }
    )

    def __init__(self, *args, **kwargs):
        """
        Garante que start_date e end_date sejam objetos date,
        mesmo se passados como string pela linha de comando.
        """
        super().__init__(*args, **kwargs)

        if isinstance(self.start_date, str):
            self.start_date = datetime.date.fromisoformat(self.start_date)
        if isinstance(self.end_date, str):
            self.end_date = datetime.date.fromisoformat(self.end_date)
        print(self.end_date)

    def start_requests(self):
        """Envia o primeiro POST para a página 1."""
        start_url_page_1 = f"{self.BASE_API_URL}?page=1"
        yield Request(
            url=start_url_page_1,
            method="POST",
            body=self.static_body_payload,
            headers={"Content-Type": "application/json"},
            callback=self.parse,
        )

    def parse(self, response):
        """Processa o JSON da API, filtra por data e cuida da paginação."""

        if response.status != 200:
            self.logger.error(
                f"Falha ao acessar a API. Status: {response.status}. URL: {response.url}"
            )
            return

        try:
            data = response.json()
            editions_data = data["data"]["editions"]
        except (exceptions.JSONDecodeError, KeyError) as e:
            self.logger.error(
                f"Erro ao processar JSON da API: {e} - URL: {response.url}"
            )
            return

        gazettes = editions_data.get("data", [])
        if not gazettes:
            self.logger.info(f"Nenhum diário encontrado na página: {response.url}")
            return

        start_date_obj = self.start_date
        end_date_obj = self.end_date

        oldest_date_in_page = None

        for item in gazettes:
            try:
                edition_date_str = item["created_at"].split("T")[0]
                edition_date = datetime.date.fromisoformat(edition_date_str)
            except (KeyError, ValueError):
                self.logger.warning(f"Não foi possível extrair a data do item: {item}")
                continue

            oldest_date_in_page = edition_date

            if not (start_date_obj <= edition_date <= end_date_obj):
                continue

            filename = item.get("file")
            if not filename:
                self.logger.warning(f"Item sem 'file': {item}")
                continue

            if filename.startswith("wp-content"):
                pdf_url = f"https://dom.barradocorda.ma.gov.br/{filename}"
            else:
                main_filename = filename.replace("_signature", "")
                pdf_url = self.BASE_PDF_URL + main_filename

            yield Gazette(
                date=edition_date,
                edition_number=str(item.get("edition_number") or ""),
                is_extra_edition=bool(item.get("extra", 0)),
                file_urls=[pdf_url],
                power="executive",
            )

        if oldest_date_in_page and oldest_date_in_page < start_date_obj:
            self.logger.info(
                "Data mais antiga da página é anterior ao start_date. Parando paginação."
            )
            return

        next_page_url = editions_data.get("next_page_url")
        if next_page_url:
            yield Request(
                url=next_page_url,
                method="POST",
                body=self.static_body_payload,
                headers={"Content-Type": "application/json"},
                callback=self.parse,
            )
