from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPirapozinhoSpider(DospGazetteSpider):
    TERRITORY_ID = "3539202"
    name = "sp_pirapozinho"
    code = 5089
    start_date = date(2021, 3, 5)
