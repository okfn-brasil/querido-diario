from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCaetiteSpider(BaseDoemSpider):
    TERRITORY_ID = "2905206"
    name = "ba_caetite"
    state_city_url_part = "ba/caetite"
    start_date = date(2021, 4, 27)
