import datetime

from gazette.spiders.base.siganet import SiganetSpider


class MaBalsasSpider(SiganetSpider):
    TERRITORY_ID = "2101400"
    name = "ma_balsas"
    allowed_domains = ["transparencia.balsas.ma.gov.br/"]

    start_date = datetime.date(2017, 1, 12)

    start_urls = [
        "https://transparencia.balsas.ma.gov.br/acessoInformacao/diario/diario/listarDiario"
    ]
