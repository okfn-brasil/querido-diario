from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCachoeiraSpider(BaseDoemSpider):
    TERRITORY_ID = "2904902"
    name = "ba_cachoeira_2017"
    state_city_url_part = "ba/cachoeira"
    start_date = date(2017, 1, 3)
