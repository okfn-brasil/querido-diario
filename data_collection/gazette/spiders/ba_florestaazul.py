from gazette.spiders.base import DoemGazetteSpider


class BaFlorestaAzulSpider(DoemGazetteSpider):
    TERRITORY_ID = "2911006"
    name = "ba_florestaazul"
    state_city_url_part = "ba/florestaazul"
