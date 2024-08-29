import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaZeDocaSpider(BaseSiganetSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2114007"
    name = "ma_ze_doca"
    start_date = datetime.date(2018, 6, 4)
    allowed_domains = ["transparencia.zedoca.ma.gov.br"]
    BASE_URL = "https://transparencia.zedoca.ma.gov.br/acessoInformacao/diario/diario"
