from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaSantaCruzCabraliaSpider(BaseDoemSpider):
    TERRITORY_ID = "2927705"
    name = "ba_santa_cruz_cabralia"
    state_city_url_part = "ba/santacruzcabralia"
    start_date = date(2017, 1, 9)
