import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAdustinaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2900355"
    name = "ba_adustina"
    start_date = dt.date(2017, 1, 3)
    allowed_domains = ["adustina.ba.gov.br"]
    base_url = "https://www.adustina.ba.gov.br"
