from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpJalesSpider(DospGazetteSpider):
    TERRITORY_ID = "3524808"
    name = "sp_jales"
    code = 4932
    start_date = date(2017, 8, 9)
