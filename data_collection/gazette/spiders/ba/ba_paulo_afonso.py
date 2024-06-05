from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPauloAfonsoSpider(SaiGazetteSpider):
    TERRITORY_ID = "2924009"
    name = "ba_paulo_afonso"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/pauloafonso"
    start_date = date(2009, 10, 26)
