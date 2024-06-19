import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaCoroata(BaseSiganetSpider):
    TERRITORY_ID = "2103604"
    name = "ma_coroata"
    start_date = datetime.date(2017, 7, 28)
    allowed_domains = ["coroata.ma.gov.br"]
    BASE_URL = "https://coroata.ma.gov.br/diario/diario"
