from datetime import date

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjJaperiSpider(BaseGazetteSpider):
    TERRITORY_ID = "3302270"
    name = "rj_japeri"
    allowed_domains = ["pmjaperi.geosiap.net.br"]
    start_date = date(2019, 7, 22)
    start_urls = [
        "https://pmjaperi.geosiap.net.br/portal-transparencia/api/default/publicacoes/publicacoes"
    ]

    def parse(self, response):
        for item in response.json()["publicacoes"]:
            if item["ds_publicacao_tipo"] != "DIÁRIO OFICIAL":
                continue
            date = dateparser.parse(
                item["dt_publicacao_formatado"], languages=["pt"]
            ).date()
            url = f"https://pmjaperi.geosiap.net.br/portal-transparencia/api/default/publicacoes/get_arquivo?id_publicacao={item['id_publicacao']}"
            yield Gazette(
                date=date, file_urls=[url], is_extra_edition=False, power="executive"
            )
