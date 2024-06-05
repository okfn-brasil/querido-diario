from datetime import date

from gazette.spiders.base.sai import SaiGazetteSpider


class BaAlmadinaSpider(SaiGazetteSpider):
    TERRITORY_ID = "2900900"
    name = "ba_almadina"
    allowed_domains = ["almadina.ba.gov.br"]
    base_url = "https://www.almadina.ba.gov.br"
    start_date = date(2005, 1, 3)
