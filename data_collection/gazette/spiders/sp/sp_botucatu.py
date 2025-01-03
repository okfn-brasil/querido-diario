from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpBotucatuSpider(BaseDospSpider):
    TERRITORY_ID = "3507506"
    name = "sp_botucatu"
    code = 4734
    start_date = date(2000, 1, 6)
