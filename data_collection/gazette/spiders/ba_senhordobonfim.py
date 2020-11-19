from gazette.spiders.base import DoemGazetteSpider


class BaSenhorDoBonfimSpider(DoemGazetteSpider):
    TERRITORY_ID = "2930105"
    name = "ba_senhordobonfim"
    state_city_url_part = "ba/senhordobonfim"
