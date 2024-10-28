from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAratacaSpider(BaseSaiSpider):
    TERRITORY_ID = "2902500"
    name = "ba_baianopolis"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/baianopolis"
    start_date = date(2017, 1, 17)
