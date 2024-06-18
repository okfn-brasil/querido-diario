from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnMajorSalesSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2407252"
    name = "rn_major_sales"
    allowed_domains = ["majorsales.rn.gov.br"]
    BASE_URL = "https://www.majorsales.rn.gov.br"
    start_date = date(202, 8, 4)
