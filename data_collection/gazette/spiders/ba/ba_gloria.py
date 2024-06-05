from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaGloriaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2911402"
    name = "ba_gloria"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/gloria"
    start_date = date(2015, 1, 8)
