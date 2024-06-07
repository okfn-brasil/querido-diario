from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpParapuaSpider(DospGazetteSpider):
    TERRITORY_ID = "3536000"
    name = "sp_parapua"
    code = 5055
    start_date = date(2021, 12, 23)
