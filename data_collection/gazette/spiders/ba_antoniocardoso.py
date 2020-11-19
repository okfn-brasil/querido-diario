from gazette.spiders.base import DoemGazetteSpider


class BaAntonioCardosoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2901700"
    name = "ba_antoniocardoso"
    state_city_url_part = "ba/antoniocardoso"
