import datetime
from urllib.parse import urlencode

import scrapy
import w3lib.url

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import daily_sequence


class MgBeloHorizonteSpider(BaseGazetteSpider):
    TERRITORY_ID = "3106200"

    name = "mg_belo_horizonte"
    allowed_domains = ["dom-web.pbh.gov.br"]
    start_date = datetime.date(1995, 9, 26)

    custom_settings = {"DOWNLOAD_DELAY": 0.5, "HTTPERROR_ALLOW_ALL": True}

    def start_requests(self):
        base_url = "https://api-dom.pbh.gov.br/api/v1/edicoes/buscarpublicacaopordata"

        for date in daily_sequence(self.start_date, self.end_date):
            url_params = {"data": date.strftime("%Y-%m-%d")}
            yield scrapy.Request(
                f"{base_url}?{urlencode(url_params)}",
                cb_kwargs={"gazette_date": date.date()},
            )

    def parse(self, response, gazette_date):
        self.write_to_file(response, gazette_date)
        data = response.json()

        gazettes = data["data"]
        for gazette in gazettes:
            is_extra_edition = gazette["tipo_edicao"] != "P"
            gazette_hash = gazette["documento_jornal"]["nome_minio"]
            gazette_url = (
                f"https://api-dom.pbh.gov.br/api/v1/documentos/{gazette_hash}/download"
            )

            prefix = gazette["documento_jornal"]["prefix"]
            if prefix is not None:
                gazette_url = w3lib.url.add_or_replace_parameter(
                    gazette_url, "prefix", prefix
                )

            yield Gazette(
                date=gazette_date,
                edition_number=gazette["numero_edicao"],
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive",
            )

    def write_to_file(self, response, date):
        file_name = f"{self.name}_{date}"
        with open(f"{file_name}.html", "a") as f:
            f.write(self.build_info_about_response(response))

    def build_info_about_response(self, response):
        infos_request = f"<!-- REQUEST INFO: -->\n<!-- url: {response.request.url} -->\n<!-- method: {response.request.method} -->\n<!-- meta: {response.request.meta} -->\n<!-- headers: {response.request.headers} -->\n<!-- cookies: {response.request.cookies} -->\n<!-- encoding: {response.request.encoding} -->\n<!-- body: {response.request.body} -->\n"
        infos_response = f"<!-- RESPONSE INFO: -->\n<!-- url: {response.url}-->\n<!-- status: {response.status}-->\n<!-- headers: {response.headers}-->\n<!-- flags: {response.flags}-->\n<!-- request: {response.request}-->\n<!-- certificate: {response.certificate}-->\n<!-- ip_address: {response.ip_address}-->\n<!-- protocol: {response.protocol}-->\n<!-- body:-->\n{response.text}"
        return f"{infos_request}\n{infos_response}"
