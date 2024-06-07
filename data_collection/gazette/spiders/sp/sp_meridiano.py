from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpMeridianoSpider(DospGazetteSpider):
    TERRITORY_ID = "3529609"
    name = "sp_meridiano"
    code = 4983
    start_date = date(2014, 10, 23)
