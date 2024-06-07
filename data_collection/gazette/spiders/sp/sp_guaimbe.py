from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGuaimbeSpider(DospGazetteSpider):
    TERRITORY_ID = "3517307"
    name = "sp_guaimbe"
    code = 4848
    start_date = date(2015, 9, 9)
