from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpItajobiSpider(DospGazetteSpider):
    TERRITORY_ID = "3521903"
    name = "sp_itajobi"
    code = 4901
    start_date = date(2018, 6, 14)
