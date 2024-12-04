from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaFlorestaAzulSpider(BaseDoemSpider):
    TERRITORY_ID = "2911006"
    name = "ba_floresta_azul_2017"
    state_city_url_part = "ba/florestaazul"
    start_date = date(2017, 1, 2)
