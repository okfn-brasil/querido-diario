from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpRubiaceaSpider(DospGazetteSpider):
    TERRITORY_ID = "3544400"
    name = "sp_rubiacea"
    code = 5149
    start_date = date(2017, 9, 6)
