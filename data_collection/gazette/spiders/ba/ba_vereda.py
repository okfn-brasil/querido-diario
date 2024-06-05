from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaVeredaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2933257"
    name = "ba_vereda"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/vereda"
    start_date = date(2010, 12, 30)
