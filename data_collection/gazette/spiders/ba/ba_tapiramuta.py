from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaTapiramutaSpider(BaseDoemSpider):
    TERRITORY_ID = "2931301"
    name = "ba_tapiramuta"
    state_city_url_part = "ba/tapiramuta"
    start_date = date(2021, 1, 4)
