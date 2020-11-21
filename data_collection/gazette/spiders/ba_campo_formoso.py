from gazette.spiders.base import DoemGazetteSpider


class BaCampoFormosoSpider(DoemGazetteSpider):
    TERRITORY_ID = "2906006"
    name = "ba_campo_formoso"
    state_city_url_part = "ba/campoformoso"
