from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBuritamaSpider(DospGazetteSpider):
    TERRITORY_ID = "3508108"
    name = "sp_buritama"
    code = 4741
    start_date = date(2019, 10, 22)
