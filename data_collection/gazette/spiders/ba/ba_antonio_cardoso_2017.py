from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaAntonioCardosoSpider(BaseDoemSpider):
    TERRITORY_ID = "2901700"
    name = "ba_antonio_cardoso_2017"
    state_city_url_part = "ba/antoniocardoso"
    start_date = date(2017, 1, 2)
