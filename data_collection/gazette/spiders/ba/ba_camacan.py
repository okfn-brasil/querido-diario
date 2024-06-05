from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCamacanSpider(SaiGazetteSpider):
    TERRITORY_ID = "2905602"
    name = "ba_camacan"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/camacan"
    start_date = date(2005, 8, 1)
