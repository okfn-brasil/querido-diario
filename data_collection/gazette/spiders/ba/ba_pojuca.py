from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaPojucaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2925204"
    name = "ba_pojuca"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/pojuca"
    start_date = date(2013, 1, 15)
