import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAbareSpider(SaiGazetteSpider):
    TERRITORY_ID = "2900207"
    name = "ba_abare"
    start_date = dt.date(2007, 1, 9)
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/abare"
