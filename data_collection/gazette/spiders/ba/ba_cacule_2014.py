from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCaculeSpider(BaseDoemSpider):
    TERRITORY_ID = "2905008"
    name = "ba_cacule_2014"
    state_city_url_part = "ba/cacule"
    start_date = date(2014, 1, 2)
