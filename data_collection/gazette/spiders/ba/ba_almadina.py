import datetime as dt

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAlmadinaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2900900"
    name = "ba_almadina"
    start_date = dt.date(2005, 1, 3)
    allowed_domains = ["almadina.ba.gov.br"]
    base_url = "https://www.almadina.ba.gov.br"
