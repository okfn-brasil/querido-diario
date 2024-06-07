from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSabinoSpider(DospGazetteSpider):
    TERRITORY_ID = "3544608"
    name = "sp_sabino"
    code = 5151
    start_date = date(2018, 1, 19)
