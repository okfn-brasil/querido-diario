from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCruzDasAlmasSpider(BaseDoemSpider):
    TERRITORY_ID = "2909802"
    name = "ba_cruz_das_almas"
    state_city_url_part = "ba/cruzdasalmas"
    start_date = date(2021, 4, 1)
