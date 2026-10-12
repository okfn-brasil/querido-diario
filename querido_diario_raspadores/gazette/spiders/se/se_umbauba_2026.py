from datetime import date

from gazette.spiders.base.agape import BaseAgapeSpider


class SeUmbauba2026Spider(BaseAgapeSpider):
    TERRITORY_ID = "2807600"
    name = "se_umbauba_2026"
    alias = "pmumbauba"
    start_date = date(2026, 3, 5)
