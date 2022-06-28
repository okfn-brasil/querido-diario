import base64
import datetime as dt

from scrapy import Request
from w3lib.url import add_or_replace_parameter

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MsCampoGrandeSpider(BaseGazetteSpider):
    TERRITORY_ID = "5002704"
    name = "ms_campo_grande"
    allowed_domains = ["diogrande.campogrande.ms.gov.br"]
    start_date = dt.date(1998, 1, 9)

    def start_requests(self):
        base_url = "https://diogrande.campogrande.ms.gov.br/wp-admin/admin-ajax.php?action=edicoes_json"
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")
        start = 0
        url = f"{base_url}&de={start_date}&ate={end_date}&start={start}"
        yield Request(url, cb_kwargs={"start": start})

    def parse(self, response, start):
        data_json = response.json()

        gazettes = data_json.get("data") or []
        for gazette in gazettes:
            date = dt.datetime.strptime(gazette["dia"], "%Y-%m-%d").date()

            if date < self.start_date:
                return

            day_id = gazette["codigodia"]
            url_key = f'{{"codigodia":{day_id}}}'
            url_code = base64.b64encode(url_key.encode()).decode()
            url = f"https://diogrande.campogrande.ms.gov.br/download_edicao/{url_code}.pdf"

            edition_number = gazette["numero"]
            title = gazette["desctpd"]
            is_extra_edition = "extra" in title.lower()
            yield Gazette(
                file_urls=[url],
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        if start == 0:
            total_items = int(data_json["recordsTotal"])
            total_pages = total_items // 10  # We receive 10 results per request

            for page in range(total_pages):
                new_start = page * 10
                page_url = add_or_replace_parameter(response.url, "start", new_start)
                yield Request(page_url, cb_kwargs={"start": new_start})
