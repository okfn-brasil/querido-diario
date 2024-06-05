from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaItacareSpider(SaiGazetteSpider):
    TERRITORY_ID = "2914901"
    name = "ba_itacare"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/itacare"
    start_date = date(2005, 5, 4)
