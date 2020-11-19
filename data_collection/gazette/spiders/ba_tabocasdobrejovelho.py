from gazette.spiders.base import DoemGazetteSpider


class BaTabocasDoBrejoVelhoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2930907"
    name = "ba_tabocasdobrejovelho"
    state_city_url_part = "ba/tabocasdobrejovelho"
