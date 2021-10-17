import datetime
from urllib.parse import urlencode

import scrapy
from dateutil.rrule import DAILY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgBeloHorizonteSpider(BaseGazetteSpider):
    TERRITORY_ID = "3106200"

    name = "mg_belo_horizonte"
    allowed_domains = ["dom-web.pbh.gov.br"]
    start_date = datetime.date(1995, 9, 26)

    custom_settings = {"DOWNLOAD_DELAY": 0.5}

    def start_requests(self):
        base_url = "https://api-dom.pbh.gov.br/api/v1/edicoes/buscarpublicacaopordata"

        for date in rrule(freq=DAILY, dtstart=self.start_date, until=self.end_date):
            url_params = {"data": date.strftime("%Y-%m-%d")}
            yield scrapy.Request(
                f"{base_url}?{urlencode(url_params)}",
                cb_kwargs={"gazette_date": date.date()},
            )

    def parse(self, response, gazette_date):
        data = response.json()

        gazettes = data["data"]
        for gazette in gazettes:
            is_extra_edition = gazette["tipo_edicao"] != "P"

            gazette_hash = gazette["documento_jornal"]["nome_minio"]
            gazette_url = (
                f"https://api-dom.pbh.gov.br/api/v1/documentos/{gazette_hash}/download"
            )

            yield Gazette(
                date=gazette_date,
                edition_number=gazette["numero_edicao"],
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive",
            )
