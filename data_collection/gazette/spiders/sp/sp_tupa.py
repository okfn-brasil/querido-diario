from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTupaSpider(DospGazetteSpider):
    TERRITORY_ID = "3555000"
    name = "sp_tupa"
    code = 5267
    start_date = date(2021, 10, 2)
