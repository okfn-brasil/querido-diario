from gazette.spiders.base import DoemGazetteSpider


class BaBanzaeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2902658"
    name = "ba_banzae"
    state_city_url_part = "ba/banzae"
