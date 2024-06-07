from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpOrindiuvaSpider(DospGazetteSpider):
    TERRITORY_ID = "3534203"
    name = "sp_orindiuva"
    code = 5036
    start_date = date(2015, 3, 16)
