from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpCunhaSpider(BaseDospSpider):
    TERRITORY_ID = "3513603"
    name = "sp_cunha"
    code = 4800
    start_date = date(2021, 10, 19)
