from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaLajedaoSpider(BaseDoemSpider):
    TERRITORY_ID = "2918902"
    name = "ba_lajedao"
    state_city_url_part = "ba/lajedao"
    start_date = date(2021, 4, 14)
