import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaLauroDeFreitasSpider(SaiGazetteSpider):
    TERRITORY_ID = "2919207"
    name = "ba_lauro_de_freitas"
    start_date = dt.date(2013, 7, 31)
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/laurodefreitas"
