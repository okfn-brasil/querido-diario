from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCatolandiaSpider(BaseDoemSpider):
    TERRITORY_ID = "2907400"
    name = "ba_catolandia_2015"
    state_city_url_part = "ba/catolandia"
    start_date = date(2015, 5, 6)
