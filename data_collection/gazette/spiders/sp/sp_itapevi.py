from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpItapeviSpider(DospGazetteSpider):
    TERRITORY_ID = "3522505"
    name = "sp_itapevi"
    code = 4908
    start_date = date(2018, 12, 21)
