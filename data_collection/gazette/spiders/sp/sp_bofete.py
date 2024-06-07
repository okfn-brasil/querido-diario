from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpBofeteSpider(DospGazetteSpider):
    TERRITORY_ID = "3506904"
    name = "sp_bofete"
    code = 4726
    start_date = date(2021, 5, 24)
