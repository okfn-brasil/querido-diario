from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaTeixeiraDeFreitasSpider(BaseDoemSpider):
    TERRITORY_ID = "2931350"
    name = "ba_teixeira_de_freitas_2021"
    state_city_url_part = "ba/teixeiradefreitas"
    start_date = date(2021, 3, 2)
