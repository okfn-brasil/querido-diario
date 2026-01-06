from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaLajeSpider(BaseDoemSpider):
    TERRITORY_ID = "2918803"
    name = "ba_laje"
    state_city_url_part = "ba/laje"
    start_date = date(2020, 1, 8)
