from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCandeiasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2906501"
    name = "ba_candeias"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/candeias"
    start_date = date(2011, 1, 8)
