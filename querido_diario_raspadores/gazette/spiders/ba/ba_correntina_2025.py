from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaCorrentinaSpider(BaseDoemSpider):
    TERRITORY_ID = "2909307"
    name = "ba_correntina_2025"
    state_city_url_part = "ba/correntina"
    start_date = date(2025, 1, 1)
