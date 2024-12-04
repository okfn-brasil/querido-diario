from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class CeHorizonteSpider(BaseDospSpider):
    TERRITORY_ID = "2305233"
    name = "ce_horizonte"
    code = 687
    start_date = date(2023, 7, 3)
