from gazette.spiders.base import DoemGazetteSpider


class BaTeixeiraDeFreitasSpider(DoemGazetteSpider):
    TERRITORY_ID = "2931350"
    name = "ba_teixeiradefreitas"
    state_city_url_part = "ba/teixeiradefreitas"
