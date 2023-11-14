from gazette.spiders.base.doem import DoemGazetteSpider
from datetime import date


class BaCiceroDantasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2907806"
    name = "ba_cicero_dantas"
    start_date = date(2018, 1, 2)
    state_city_url_part = "ba/cicerodantas"
