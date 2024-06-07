from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpIrapuaSpider(DospGazetteSpider):
    TERRITORY_ID = "3521507"
    name = "sp_irapua"
    code = 4897
    start_date = date(2021, 7, 1)
