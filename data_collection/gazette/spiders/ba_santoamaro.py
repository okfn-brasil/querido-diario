from gazette.spiders.base import DoemGazetteSpider


class BaSantoAmaroSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928604"
    name = "ba_santoamaro"
    state_city_url_part = "ba/santoamaro"
