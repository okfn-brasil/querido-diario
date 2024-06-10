from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJaborandiSpider(SaiGazetteSpider):
    TERRITORY_ID = "2917359"
    name = "ba_jaborandi"
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/jaborandi"
    start_date = date(2022, 3, 4)
