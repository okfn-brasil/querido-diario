from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeCariraSpider(BaseAgapeSpider):
    TERRITORY_ID = "2801405"
    name = "se_carira"
    alias = "pmcarira"
    start_date = date(2011, 9, 14)
