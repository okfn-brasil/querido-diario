from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpTabapuaSpider(DospGazetteSpider):
    TERRITORY_ID = "3552601"
    name = "sp_tabapua"
    code = 5237
    start_date = date(2018, 6, 11)
