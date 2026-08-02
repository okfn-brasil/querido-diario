from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaIpiauSpider(BaseDoemSpider):
    TERRITORY_ID = "2913903"
    name = "ba_ipiau"
    state_city_url_part = "ba/ipiau"
    start_date = date(2016, 5, 9)
