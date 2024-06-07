from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCabreuvaSpider(DospGazetteSpider):
    TERRITORY_ID = "3508405"
    name = "sp_cabreuva"
    code = 4744
    start_date = date(2021, 12, 16)
