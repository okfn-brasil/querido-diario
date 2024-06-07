from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class MgIturamaSpider(DospGazetteSpider):
    TERRITORY_ID = "3134400"
    name = "mg_iturama"
    code = 1929
    start_date = date(2021, 9, 3)
