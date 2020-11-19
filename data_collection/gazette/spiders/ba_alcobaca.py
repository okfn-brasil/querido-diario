from gazette.spiders.base import DoemGazetteSpider


class BaAlcobacaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2900801"
    name = "ba_alcobaca"
    state_city_url_part = "ba/alcobaca"
