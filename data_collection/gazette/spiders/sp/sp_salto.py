from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSaltoSpider(DospGazetteSpider):
    TERRITORY_ID = "3545209"
    name = "sp_salto"
    code = 5158
    start_date = date(2018, 2, 1)
