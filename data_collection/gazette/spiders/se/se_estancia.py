from gazette.spiders.base.sai import SaiGazetteSpider


class SeEstanciaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2802106"
    name = "se_estancia"
    base_url = "https://www.estancia.se.gov.br"
