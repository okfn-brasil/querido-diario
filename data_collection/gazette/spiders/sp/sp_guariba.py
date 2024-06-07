from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGuaribaSpider(DospGazetteSpider):
    TERRITORY_ID = "3518602"
    name = "sp_guariba"
    code = 4861
    start_date = date(2018, 7, 6)
