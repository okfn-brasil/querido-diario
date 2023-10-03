from gazette.spiders.base.sai import SaiGazetteSpider


class BaJeremoaboSpider(SaiGazetteSpider):
    TERRITORY_ID = "2918100"
    name = "ba_jeremoabo"
    state_city_url_part = ""
    base_url = "https://www.jeremoabo.ba.gov.br"
