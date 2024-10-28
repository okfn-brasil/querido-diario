from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAratacaSpider(BaseSaiSpider):
    TERRITORY_ID = "2902302"
    name = "ba_aratuipe"
    allowed_domains = ["aratuipe.ba.gov.br"]
    base_url = "https://www.aratuipe.ba.gov.br"
    start_date = date(2013, 1, 10)
