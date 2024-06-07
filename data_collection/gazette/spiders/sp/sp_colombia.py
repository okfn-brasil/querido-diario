from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpColombiaSpider(DospGazetteSpider):
    TERRITORY_ID = "3512100"
    name = "sp_colombia"
    code = 4785
    start_date = date(2017, 1, 12)
