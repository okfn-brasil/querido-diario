from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCampoAlegreDeLourdesSpider(BaseDoemSpider):
    TERRITORY_ID = "2905909"
    name = "ba_campo_alegre_de_lourdes"
    state_city_url_part = "ba/campoalegredelourdes"
    start_date = date(2020, 11, 30)
