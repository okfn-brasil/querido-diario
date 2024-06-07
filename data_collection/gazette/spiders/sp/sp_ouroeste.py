from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpOuroesteSpider(DospGazetteSpider):
    TERRITORY_ID = "3534757"
    name = "sp_ouroeste"
    code = 5043
    start_date = date(2021, 5, 3)
