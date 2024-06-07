from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpUrupesSpider(DospGazetteSpider):
    TERRITORY_ID = "3556008"
    name = "sp_urupes"
    code = 5278
    start_date = date(2021, 7, 15)
