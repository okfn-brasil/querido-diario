from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCastroAlvesSpider(SaiGazetteSpider):
    TERRITORY_ID = "2907301"
    name = "ba_castro_alves"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/castroalves"
    start_date = date(2005, 3, 22)
