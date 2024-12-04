import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaVianaSpider(BaseSiganetSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2112803"
    name = "ma_viana"
    start_date = datetime.date(2018, 1, 18)
    allowed_domains = ["transparencia.viana.ma.gov.br"]
    BASE_URL = "https://transparencia.viana.ma.gov.br/acessoInformacao/diario/diario"
