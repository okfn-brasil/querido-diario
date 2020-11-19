from gazette.spiders.base import DoemGazetteSpider


class BaSentoSeSpider(DoemGazetteSpider):
    TERRITORY_ID = "2930204"
    name = "ba_sentose"
    state_city_url_part = "ba/sentose"
