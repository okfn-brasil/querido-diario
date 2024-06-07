from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBalbinosSpider(DospGazetteSpider):
    TERRITORY_ID = "3504701"
    name = "sp_balbinos"
    code = 4702
    start_date = date(2018, 2, 2)
