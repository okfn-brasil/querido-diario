from gazette.spiders.base import DoemGazetteSpider


class BaCiceroDantasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2907806"
    name = "ba_cicerodantas"
    state_city_url_part = "ba/cicerodantas"
