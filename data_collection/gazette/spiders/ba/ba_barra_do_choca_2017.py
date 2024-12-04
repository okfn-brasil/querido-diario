from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaBarraDoChocaSpider(BaseDoemSpider):
    TERRITORY_ID = "2902906"
    name = "ba_barra_do_choca_2017"
    state_city_url_part = "ba/barradochoca"
    start_date = date(2017, 6, 9)
