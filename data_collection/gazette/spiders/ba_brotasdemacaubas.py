from gazette.spiders.base import DoemGazetteSpider


class BaBrotasDeMacaubasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2904506"
    name = "ba_brotasdemacaubas"
    state_city_url_part = "ba/brotasdemacaubas"
