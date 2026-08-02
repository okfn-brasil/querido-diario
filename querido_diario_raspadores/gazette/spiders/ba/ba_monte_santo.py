from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaMonteSantoSpider(BaseDoemSpider):
    TERRITORY_ID = "2921500"
    name = "ba_monte_santo"
    state_city_url_part = "ba/montesanto"
    start_date = date(2021, 1, 2)
