from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCiceroDantasSpider(BaseDoemSpider):
    TERRITORY_ID = "2907806"
    name = "ba_cicero_dantas"
    state_city_url_part = "ba/cicerodantas"
    start_date = date(2012, 1, 3)
