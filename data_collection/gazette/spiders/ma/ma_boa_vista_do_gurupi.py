import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaBoaVistaDoGurupiSpider(BaseSiganetSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2101970"
    name = "ma_boa_vista_do_gurupi"
    start_date = datetime.date(2019, 7, 3)
    allowed_domains = ["transparencia.boavistadogurupi.ma.gov.br"]
    BASE_URL = "https://transparencia.boavistadogurupi.ma.gov.br/acessoInformacao/diario/diario"
