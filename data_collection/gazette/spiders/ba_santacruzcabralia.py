from gazette.spiders.base import DoemGazetteSpider


class BaSantaCruzCabraliaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2927705"
    name = "ba_santacruzcabralia"
    state_city_url_part = "ba/santacruzcabralia"
