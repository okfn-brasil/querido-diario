import re
from datetime import date

import dateutil
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpJacareiSpider(BaseGazetteSpider):
    TERRITORY_ID = "3524402"
    name = "sp_jacarei"
    allowed_domains = [
        "boletinsoficiais.geosiap.net",
        "geosiap.s3-sa-east-1.amazonaws.com",
    ]
    base_url = "https://boletinsoficiais.geosiap.net/api/pmjacarei/publicacao/bo_arquivos_public?inativos=false"
    start_date = date(2004, 3, 27)

    def start_requests(self):
        url = self.base_url
        url += f'&dt_inicial={self.start_date.strftime("%Y-%m-%d")}&dt_final={self.end_date.strftime("%Y-%m-%d")}'

        yield Request(url, callback=self.parse_info)

    def parse_info(self, response):
        data = response.json()["data"]
        for gazzete in data:
            url = f'https://boletinsoficiais.geosiap.net/api/pmjacarei/publicacao/get_url_arquivo/{gazzete["id"]}'
            yield Request(url, meta=gazzete)

    def parse(self, response):
        gazzete = response.meta
        gazzete_date = dateutil.parser.isoparse(gazzete["dt_publicacao"]).date()
        match = re.findall("(\d+)", gazzete["nome_arquivo"])
        gazzete_number = match[0] if match else ""
        gazzete_url = response.json()["url"]

        yield Gazette(
            date=gazzete_date,
            edition_number=gazzete_number,
            file_urls=[gazzete_url],
            is_extra_edition=gazzete_number == "",
            power="executive_legislative",
        )
