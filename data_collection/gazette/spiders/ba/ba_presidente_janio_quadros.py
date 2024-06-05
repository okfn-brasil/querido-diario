from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPresidenteJanioQuadrosSpider(SaiGazetteSpider):
    TERRITORY_ID = "2925709"
    name = "ba_presidente_janio_quadros"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/presidentejanioquadros"
    start_date = date(2009, 1, 13)
