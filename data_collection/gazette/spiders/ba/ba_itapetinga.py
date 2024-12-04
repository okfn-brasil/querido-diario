from datetime import date

from gazette.spiders.base.doem import BaseDoemSpider


class BaItapetingaSpider(BaseDoemSpider):
    TERRITORY_ID = "2916401"
    name = "ba_itapetinga"
    state_city_url_part = "ba/itapetinga"
    start_date = date(2010, 1, 4)
