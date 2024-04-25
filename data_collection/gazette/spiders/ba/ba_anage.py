import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAnageSpider(SaiGazetteSpider):
    TERRITORY_ID = "2901205"
    name = "ba_anage"
    start_date = dt.date(2017, 1, 12)
    allowed_domains = ["anage.ba.gov.br"]
    base_url = "https://anage.ba.gov.br"
