from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeParamotiSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2310407"
    name = "ce_paramoti"
    allowed_domains = ["paramoti.ce.gov.br"]
    BASE_URL = "https://www.paramoti.ce.gov.br"
    start_date = date(2023, 1, 2)
