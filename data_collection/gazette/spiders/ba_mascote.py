from gazette.spiders.base import DoemGazetteSpider


class BaMascoteSpider(DoemGazetteSpider):
    TERRITORY_ID = "2920908"
    name = "ba_mascote"
    state_city_url_part = "ba/mascote"
