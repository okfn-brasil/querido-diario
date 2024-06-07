from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpRiolandiaSpider(DospGazetteSpider):
    TERRITORY_ID = "3544202"
    name = "sp_riolandia"
    code = 5145
    start_date = date(2014, 5, 7)
