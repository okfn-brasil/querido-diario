from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaSentoSeSpider(BaseDoemSpider):
    TERRITORY_ID = "2930204"
    name = "ba_sento_se"
    state_city_url_part = "ba/sentose"
    start_date = date(2017, 1, 2)
