from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaBrotasDeMacaubasSpider(BaseDoemSpider):
    TERRITORY_ID = "2904506"
    name = "ba_brotas_de_macaubas"
    state_city_url_part = "ba/brotasdemacaubas"
    start_date = date(2019, 8, 13)
