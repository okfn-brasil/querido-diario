from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSantaFeDoSulSpider(DospGazetteSpider):
    TERRITORY_ID = "3546603"
    name = "sp_santa_fe_do_sul"
    code = 5172
    start_date = date(2021, 12, 2)
