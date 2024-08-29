import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaSaoVicenteFerrerSpider(BaseSiganetSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2111706"
    name = "ma_sao_vicente_ferrer"
    start_date = datetime.date(2021, 4, 26)
    allowed_domains = ["saovicenteferrer.ma.gov.br"]
    BASE_URL = "https://saovicenteferrer.ma.gov.br/diario/diario"
