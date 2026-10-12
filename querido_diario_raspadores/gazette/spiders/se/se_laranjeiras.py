from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeLaranjeirasSpider(BaseAgapeSpider):
    TERRITORY_ID = "2803609"
    name = "se_laranjeiras"
    alias = "pmlaranjeiras"
    start_date = date(2021, 1, 4)
