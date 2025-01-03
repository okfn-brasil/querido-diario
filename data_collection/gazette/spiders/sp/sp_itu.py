from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpItuSpider(BaseDospSpider):
    TERRITORY_ID = "3523909"
    name = "sp_itu"
    code = 4923
    start_date = date(2019, 8, 15)
