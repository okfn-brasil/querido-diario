from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaIcatuSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2105104"
    name = "ma_icatu"
    allowed_domains = ["icatu.ma.gov.br"]
    BASE_URL = "https://www.icatu.ma.gov.br"
    start_date = date(2021, 3, 29)
