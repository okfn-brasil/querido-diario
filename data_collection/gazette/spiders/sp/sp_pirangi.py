from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPirangiSpider(DospGazetteSpider):
    TERRITORY_ID = "3539004"
    name = "sp_pirangi"
    code = 5087
    start_date = date(2015, 9, 18)
