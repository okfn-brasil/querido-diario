import datetime

from gazette.spiders.base.siganet import BaseSiganetSpider


class MaBacuri(BaseSiganetSpider):
    TERRITORY_ID = "2101301"
    name = "ma_bacuri"
    start_date = datetime.date(2017, 3, 30)
    BASE_URL = "https://bacuri.ma.gov.br/diario/diario"
