from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCaiabuSpider(DospGazetteSpider):
    TERRITORY_ID = "3508900"
    name = "sp_caiabu"
    code = 4749
    start_date = date(2018, 11, 13)
