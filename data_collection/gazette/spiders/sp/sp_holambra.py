from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpHolambraSpider(DospGazetteSpider):
    TERRITORY_ID = "3519055"
    name = "sp_holambra"
    code = 4867
    start_date = date(2017, 5, 3)
