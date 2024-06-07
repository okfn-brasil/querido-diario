from datetime import date

from gazette.spiders.base.dosp import DospGazetteSpider


class SpQuataSpider(DospGazetteSpider):
    TERRITORY_ID = "3541703"
    name = "sp_quata"
    code = 5119
    start_date = date(2017, 12, 13)
