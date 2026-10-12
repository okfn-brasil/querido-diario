from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeJapoataSpider(BaseAgapeSpider):
    TERRITORY_ID = "2803401"
    name = "se_japoata"
    alias = "pmjapoata"
    start_date = date(1997, 2, 18)
