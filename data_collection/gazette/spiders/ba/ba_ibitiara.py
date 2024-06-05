from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaIbitiaraSpider(SaiGazetteSpider):
    TERRITORY_ID = "2913002"
    name = "ba_ibitiara"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/ibitiara"
    start_date = date(2013, 1, 8)
