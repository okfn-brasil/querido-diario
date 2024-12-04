from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpCatanduvaSpider(BaseDospSpider):
    TERRITORY_ID = "3511102"
    name = "sp_catanduva"
    code = 4775
    start_date = date(2016, 3, 18)
