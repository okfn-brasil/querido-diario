from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaArameSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2100956"
    name = "ma_arame"
    allowed_domains = ["arame.ma.gov.br"]
    BASE_URL = "https://www.arame.ma.gov.br"
    start_date = date(2017, 2, 10)
