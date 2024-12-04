import datetime as dt

from gazette.spiders.base.sai import BaseSaiSpider


class BaMaragogipeSpider(BaseSaiSpider):
    TERRITORY_ID = "2920601"
    name = "ba_maragogipe"
    start_date = dt.date(2011, 2, 2)
    allowed_domains = ["sai.io.org.br"]
    base_url = "https://sai.io.org.br/ba/maragojipe"
