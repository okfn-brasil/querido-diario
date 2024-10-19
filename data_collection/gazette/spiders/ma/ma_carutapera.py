from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaCarutaperaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2102903"
    name = "ma_carutapera"
    allowed_domains = ["carutapera.ma.gov.br"]
    BASE_URL = "https://www.carutapera.ma.gov.br"
    start_date = date(2021, 2, 18)
