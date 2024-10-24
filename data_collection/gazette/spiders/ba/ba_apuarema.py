from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaApuaremaSpider(BaseSaiSpider):
    TERRITORY_ID = "2901957"
    name = "ba_apuarema"
    allowed_domains = ["apuarema.ba.gov.br"]
    base_url = "https://www.apuarema.ba.gov.br"
    start_date = date(2009, 1, 23)
