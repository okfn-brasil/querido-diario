from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpDirceReisSpider(BaseDospSpider):
    TERRITORY_ID = "3513850"
    name = "sp_dirce_reis"
    code = 4803
    start_date = date(2019, 4, 4)
