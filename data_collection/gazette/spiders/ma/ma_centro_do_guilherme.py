import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaCentroDoGuilhermeSpider(BaseSiganetSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2103158"
    name = "ma_centro_do_guilherme"
    start_date = datetime.date(2021, 3, 12)
    allowed_domains = ["transparencia.centrodoguilherme.ma.gov.br"]
    BASE_URL = "https://transparencia.centrodoguilherme.ma.gov.br/acessoInformacao/diario/diario"
