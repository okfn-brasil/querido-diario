from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaTrizidelaDoValeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2112233"
    name = "ma_trizidela_do_vale"
    allowed_domains = ["trizideladovale.ma.gov.br"]
    BASE_URL = "https://www.trizideladovale.ma.gov.br"
    start_date = date(2015, 12, 9)
