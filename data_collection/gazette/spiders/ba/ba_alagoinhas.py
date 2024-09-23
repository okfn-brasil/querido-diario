from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaAlagoinhasSpider(BaseDoemSpider):
    TERRITORY_ID = "2900702"
    name = "ba_alagoinhas"
    state_city_url_part = "ba/alagoinhas"
    start_date = date(2015, 1, 28)
