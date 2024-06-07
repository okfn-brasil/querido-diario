from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPardinhoSpider(DospGazetteSpider):
    TERRITORY_ID = "3536109"
    name = "sp_pardinho"
    code = 5056
    start_date = date(2019, 7, 31)
