from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpRioClaroSpider(BaseDospSpider):
    TERRITORY_ID = "3543907"
    name = "sp_rio_claro"
    code = 5142
    start_date = date(2023, 6, 21)
