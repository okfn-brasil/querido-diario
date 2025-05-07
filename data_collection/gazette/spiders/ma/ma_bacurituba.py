import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaBacurituba(BaseSiganetSpider):
    TERRITORY_ID = "2101350"
    name = "ma_bacurituba"
    start_date = datetime.date(2018, 4, 6)
    BASE_URL = "https://bacurituba.ma.gov.br/diario/diario"
