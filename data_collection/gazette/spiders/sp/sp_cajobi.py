from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCajobiSpider(DospGazetteSpider):
    TERRITORY_ID = "3509304"
    name = "sp_cajobi"
    code = 4754
    start_date = date(2013, 6, 10)
