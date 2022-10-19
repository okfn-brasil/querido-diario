import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaBalsasSpider(BaseGazetteSpider):
    TERRITORY_ID = "2101400"
    name = "ma_balsas"
    allowed_domains = ["transparencia.balsas.ma.gov.br/"]

    start_date = datetime.date(2017, 1, 12)
    end_date = datetime.date.today()

    start_urls = [
        "https://transparencia.balsas.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    ]

    def parse(self, response):
        for gazette in response.json()["data"]:
            gazette_date = datetime.datetime.strptime(
                gazette["TDI_DT_PUBLICACAO"], "%Y-%m-%d %H:%M:%S"
            ).date()

            if self.end_date < gazette_date:
                break
            if self.start_date > gazette_date:
                continue

            if gazette_date.year > 2017:
                x = "0000000002"
            else:
                x = "0000000424"

            pdf_url = f"https://painel.siganet.net.br/upload/{x}/cms/publicacoes/diario/{gazette['TDI_ARQUIVO']}"

            yield Gazette(
                date=gazette_date,
                file_urls=[pdf_url],
                is_extra_edition=False,
                edition_number=gazette["TDI_EDICAO"],
                power="executive",
            )
