import base64
import datetime as dt
import re

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MsCampoGrandeSpider(BaseGazetteSpider):
    TERRITORY_ID = "5002704"
    name = "ms_campo_grande"
    allowed_domains = ["diogrande.campogrande.ms.gov.br"]
    start_date = dt.date(1998, 1, 9)

    def start_requests(self):
        base_url = "https://diogrande.campogrande.ms.gov.br/wp-admin/admin-ajax.php?action=edicoes_json"
        initial_date = self.start_date.strftime("%d/%m/%Y")
        final_date = self.end_date.strftime("%d/%m/%Y")
        url = f"{base_url}&de={initial_date}&ate{final_date}&start=0"
        yield Request(url)

    def parse(self, response, sequential=0):
        data_json = response.json()["data"]
        if not isinstance(data_json, list):
            return
        for entry in data_json:
            date = dt.datetime.strptime(entry["dia"], "%Y-%m-%d").date()

            if date < self.start_date:
                return

            day_id = entry["codigodia"]
            url_key = f'{{"codigodia":{day_id}}}'
            url_code = base64.b64encode(url_key.encode()).decode()
            url = f"https://diogrande.campogrande.ms.gov.br/download_edicao/{url_code}.pdf"

            edition_number = entry["numero"]
            title = entry["desctpd"]
            is_extra_edition = "extra" in title.lower()
            yield Gazette(
                file_urls=[url],
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        next_sequential = sequential + 10
        next_url = re.sub(r"start=(\d+)", f"start={next_sequential}", response.url)
        yield Request(next_url, cb_kwargs={"sequential": next_sequential})
