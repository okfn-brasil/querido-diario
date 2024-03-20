import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaJeremoaboSpider(SaiGazetteSpider):
    TERRITORY_ID = "2918100"
    name = "ba_jeremoabo"
    start_date = dt.date(2016, 4, 28)
    allowed_domains = ["jeremoabo.ba.gov.br"]
    base_url = "https://www.jeremoabo.ba.gov.br"
