from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaSantaBrigidaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2927606"
    name = "ba_santa_brigida"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/santabrigida"
    start_date = date(2007, 1, 29)
