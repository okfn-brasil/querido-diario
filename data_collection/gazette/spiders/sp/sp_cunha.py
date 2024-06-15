from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpCunhaSpider(DospGazetteSpider):
    TERRITORY_ID = "3513603"
    name = "sp_cunha"
    code = 4800
    start_date = date(2021, 10, 19)
