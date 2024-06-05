from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaMarauSpider(SaiGazetteSpider):
    TERRITORY_ID = "2920700"
    name = "ba_marau"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/marau"
    start_date = date(2008, 4, 4)
