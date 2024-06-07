from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpLinsSpider(DospGazetteSpider):
    TERRITORY_ID = "3527108"
    name = "sp_lins"
    code = 4956
    start_date = date(2017, 12, 21)
