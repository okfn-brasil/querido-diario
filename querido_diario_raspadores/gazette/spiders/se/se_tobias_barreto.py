from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeTobiasBarretoSpider(BaseAgapeSpider):
    TERRITORY_ID = "2807402"
    name = "se_tobias_barreto"
    alias = "pmtobiasbarreto"
    start_date = date(2013, 1, 24)
