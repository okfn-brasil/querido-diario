from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCanudosSpider(BaseDoemSpider):
    TERRITORY_ID = "2906824"
    name = "ba_canudos"
    state_city_url_part = "ba/canudos"
    start_date = date(2013, 1, 4)
