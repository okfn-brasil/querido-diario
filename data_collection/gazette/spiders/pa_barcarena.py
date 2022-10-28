from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PaBarcarenaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1501303"
    name = "pa_barcarena"
    allowed_domains = ["domapi.tecnologia.ws"]
    start_urls = ["http://domapi.tecnologia.ws/diario/consulta"]

    start_date = date(2021, 11, 8)

    def start_requests(self):

        query = f'?data_ini={self.start_date.strftime("%Y/%m/%d")}&data_fim={self.end_date.strftime("%Y/%m/%d")}&edicao=&palavra_chave='

        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
        }
        for url in self.start_urls:
            yield scrapy.Request(f"{url}{query}", headers=header)

    def parse(self, response):

        json_response = response.json()
        processed_data = set()
        processed_url = set()

        for lines in json_response:

            edition_id = lines["id_diario"].strip()
            edition_number = lines["edicao"].strip()
            url = lines["endereco"].replace("\\", "").strip()
            edition_date = datetime.strptime(
                lines["data_publicacao"], "%Y-%m-%d %H:%M:%S"
            ).date()

            edition_data = (edition_id, edition_number, url, edition_date)

            if edition_data in processed_data:
                self.logger.info(f"Skipping duplicate data: {edition_data}")
                continue

            if url in processed_url:
                self.logger.info(f"Skipping duplicate url: {edition_data}")
                continue

            processed_data.add(edition_data)
            processed_url.add(url)

            yield Gazette(
                date=edition_date,
                edition_number=edition_id,
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                power="executive",
                file_urls=[url],
            )
