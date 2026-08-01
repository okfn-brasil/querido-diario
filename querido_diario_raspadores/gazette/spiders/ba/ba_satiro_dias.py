from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaSatiroDiasSpider(BaseDoemSpider):
    TERRITORY_ID = "2929701"
    name = "ba_satiro_dias"
    state_city_url_part = "ba/satirodias"
    start_date = date(2021, 3, 30)
