from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBoraceiaSpider(DospGazetteSpider):
    TERRITORY_ID = "3507308"
    name = "sp_boraceia"
    code = 4731
    start_date = date(2024, 2, 5)
