from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpArealvaSpider(DospGazetteSpider):
    TERRITORY_ID = "3503406"
    name = "sp_arealva"
    code = 4688
    start_date = date(2017, 10, 9)
