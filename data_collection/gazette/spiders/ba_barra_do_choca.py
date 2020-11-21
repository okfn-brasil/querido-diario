from gazette.spiders.base import DoemGazetteSpider


class BaBarraDoChocaSpider(DoemGazetteSpider):
    TERRITORY_ID = "2902906"
    name = "ba_barra_do_choca"
    state_city_url_part = "ba/barradochoca"
