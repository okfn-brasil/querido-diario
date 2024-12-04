import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseSiganetSpider(BaseGazetteSpider):
    def start_requests(self):
        yield scrapy.Request(f"{self.BASE_URL}/listarDiario")

    def parse(self, response):
        for gazette in response.json()["data"]:
            gazette_date = datetime.datetime.strptime(
                gazette["TDI_DT_PUBLICACAO"], "%Y-%m-%d %H:%M:%S"
            ).date()

            file_id = gazette["TDI_TPS_ID"].zfill(10)
            gazette_url = f"https://painel.siganet.net.br/upload/{file_id}/cms/publicacoes/diario/{gazette['TDI_ARQUIVO']}"

            if self.start_date <= gazette_date <= self.end_date:
                yield Gazette(
                    date=gazette_date,
                    file_urls=[gazette_url],
                    edition_number=gazette["TDI_EDICAO"],
                    power="executive_legislative",
                )
