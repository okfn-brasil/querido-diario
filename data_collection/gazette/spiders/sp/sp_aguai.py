from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAguaiSpider(BaseDospSpider):
    TERRITORY_ID = "3500303"
    name = "sp_aguai"
    code = 4651
    start_date = date(2022, 10, 19)
