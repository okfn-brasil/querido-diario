from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpUraniaSpider(DospGazetteSpider):
    TERRITORY_ID = "3555802"
    name = "sp_urania"
    code = 5276
    start_date = date(2020, 1, 14)
