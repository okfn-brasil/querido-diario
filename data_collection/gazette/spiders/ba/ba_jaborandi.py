import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJaborandiSpider(SaiGazetteSpider):
    TERRITORY_ID = "2917359"
    name = "ba_jaborandi"
    start_date = dt.date(2022, 3, 4)
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/jaborandi"
