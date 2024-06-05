from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaGanduSpider(SaiGazetteSpider):
    TERRITORY_ID = "2911204"
    name = "ba_gandu"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/gandu"
    start_date = date(2009, 1, 20)
