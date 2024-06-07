from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpJaciSpider(DospGazetteSpider):
    TERRITORY_ID = "3524501"
    name = "sp_jaci"
    code = 4929
    start_date = date(2017, 9, 22)
