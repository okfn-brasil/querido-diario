from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCatuSpider(SaiGazetteSpider):
    TERRITORY_ID = "2907509"
    name = "ba_catu"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/catu"
    start_date = date(2005, 11, 30)
