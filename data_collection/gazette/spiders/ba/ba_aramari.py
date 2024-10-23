from datetime import date

from gazette.spiders.base.sai import BaseSaiSpider


class BaAramariSpider(BaseSaiSpider):
    TERRITORY_ID = "2902203"
    name = "ba_aramari"
    allowed_domains = ["aramari.ba.gov.br"]
    base_url = "https://www.aramari.ba.gov.br"
    start_date = date(2009, 2, 12)
