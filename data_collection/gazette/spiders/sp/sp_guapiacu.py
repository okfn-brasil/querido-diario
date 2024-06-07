from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGuapiacuSpider(DospGazetteSpider):
    TERRITORY_ID = "3517505"
    name = "sp_guapiacu"
    code = 4850
    start_date = date(2018, 12, 13)
