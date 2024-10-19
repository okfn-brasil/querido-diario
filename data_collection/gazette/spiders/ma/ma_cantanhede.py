from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaCantanhedeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2102705"
    name = "ma_cantanhede"
    allowed_domains = ["cantanhede.ma.gov.br"]
    BASE_URL = "https://www.cantanhede.ma.gov.br"
    start_date = date(2009, 1, 5)
