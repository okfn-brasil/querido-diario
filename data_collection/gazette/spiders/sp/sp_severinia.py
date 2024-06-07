from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpSeveriniaSpider(DospGazetteSpider):
    TERRITORY_ID = "3551900"
    name = "sp_severinia"
    code = 5229
    start_date = date(2017, 2, 21)
