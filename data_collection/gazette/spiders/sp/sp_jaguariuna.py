from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpJaguariunaSpider(DospGazetteSpider):
    TERRITORY_ID = "3524709"
    name = "sp_jaguariuna"
    code = 4931
    start_date = date(2019, 3, 8)
