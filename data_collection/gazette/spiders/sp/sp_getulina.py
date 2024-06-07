from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpGetulinaSpider(DospGazetteSpider):
    TERRITORY_ID = "3517000"
    name = "sp_getulina"
    code = 4845
    start_date = date(2016, 1, 4)
