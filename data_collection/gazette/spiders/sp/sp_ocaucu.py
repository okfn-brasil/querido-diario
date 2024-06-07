from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpOcaucuSpider(DospGazetteSpider):
    TERRITORY_ID = "3533700"
    name = "sp_ocaucu"
    code = 5031
    start_date = date(2018, 9, 19)
