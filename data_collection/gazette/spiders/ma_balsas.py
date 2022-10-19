import datetime
from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaBalsasSpider(BaseGazetteSpider):
    TERRITORY_ID = "2101400"
    name = "ma_balsas"
    allowed_domains = ["transparencia.balsas.ma.gov.br/"]

    start_date = datetime.date(2017, 1, 12)
    end_date = datetime.date.today()

    start_urls = ["https://transparencia.balsas.ma.gov.br/acessoInformacao/diario/diario/listarDiario"]

    BASE_URL = "https://painel.siganet.net.br/upload/{}/cms/publicacoes/diario/"

    def parse(self, response):
        data = response.json()['data']

        for gazette in data:
            gazette_date = datetime.datetime.strptime(gazette['TDI_DT_PUBLICACAO'], "%Y-%m-%d %H:%M:%S").date()
            
            if gazette_date.year > 2017:
                x = "0000000002"
            else:
                x = "0000000424"

            pdf_url = f"{self.BASE_URL.format(x)}{gazette['TDI_ARQUIVO']}"

            if self.end_date < gazette_date:
                continue
            if self.start_date > gazette_date:
                break

            yield Gazette(
                date=gazette_date,
                file_urls=[pdf_url],
                is_extra_edition=False,
                edition_number=gazette['TDI_EDICAO'],
                power="executive"
            )