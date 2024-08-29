import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaAxixaSpider(BaseSiganetSpider):
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "2101103"
    name = "ma_axixa"
    start_date = datetime.date(2021, 3, 31)
    allowed_domains = ["transparencia.axixa.ma.gov.br"]
    BASE_URL = "https://transparencia.axixa.ma.gov.br/acessoInformacao/diario/diario"
