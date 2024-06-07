from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpAraminaSpider(DospGazetteSpider):
    TERRITORY_ID = "3503000"
    name = "sp_aramina"
    code = 4682
    start_date = date(2022, 9, 27)
