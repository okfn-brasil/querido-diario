from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAvareSpider(BaseDospSpider):
    TERRITORY_ID = "3504503"
    name = "sp_avare"
    code = 4700
    start_date = date(2018, 10, 3)
