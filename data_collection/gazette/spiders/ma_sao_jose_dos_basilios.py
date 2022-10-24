import datetime

from gazette.spiders.base.siganet import SiganetSpider


class MaBalsasSpider(SiganetSpider):
    TERRITORY_ID = "2111250"
    name = "ma_sao_jose_dos_basilios"
    allowed_domains = ["transparencia.saojosedosbasilios.ma.gov.br"]

    start_date = datetime.date(2015, 11, 27)
    end_date = datetime.date.today()

    start_urls = [
        "https://transparencia.saojosedosbasilios.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    ]