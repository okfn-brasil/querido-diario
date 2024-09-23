from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaSenhorDoBonfimSpider(BaseDoemSpider):
    TERRITORY_ID = "2930105"
    name = "ba_senhor_do_bonfim"
    state_city_url_part = "ba/senhordobonfim"
    start_date = date(2013, 1, 3)
