from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaMedeirosNetoSpider(BaseDoemSpider):
    TERRITORY_ID = "2921104"
    name = "ba_medeiros_neto_2018"
    start_date = date(2018, 1, 9)
    state_city_url_part = "ba/medeirosneto"
