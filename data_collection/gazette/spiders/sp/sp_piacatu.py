from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpPiacatuSpider(DospGazetteSpider):
    TERRITORY_ID = "3537701"
    name = "sp_piacatu"
    code = 5075
    start_date = date(2018, 9, 19)
