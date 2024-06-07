from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpZacariasSpider(DospGazetteSpider):
    TERRITORY_ID = "3557154"
    name = "sp_zacarias"
    code = 5293
    start_date = date(2018, 9, 21)
