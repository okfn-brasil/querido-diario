import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaCorrentinaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2909307"
    name = "ba_correntina"
    start_date = dt.date(2007, 11, 30)
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/correntina"
