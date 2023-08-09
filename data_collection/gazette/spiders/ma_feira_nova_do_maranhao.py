import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaFeiraNovaDoMaranhao(BaseSiganetSpider):
    TERRITORY_ID = "2104073"
    name = "ma_feira_nova_do_maranhao"
    start_date = datetime.date(2017, 1, 31)
    allowed_domains = ["feiranovadomaranhao.ma.gov.br"]
    BASE_URL = "https://feiranovadomaranhao.ma.gov.br/diario/diario"
