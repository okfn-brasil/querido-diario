from gazette.spiders.base import DoemGazetteSpider


class BaSantoAmaroSpider(DoemGazetteSpider):
    TERRITORY_ID = "2928604"
    name = "ba_santo_amaro"
    state_city_url_part = "ba/santoamaro"
