from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeCedroSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2303808"
    name = "ce_cedro"
    allowed_domains = ["cedro.ce.gov.br"]
    BASE_URL = "https://www.cedro.ce.gov.br"
    start_date = date(202, 6, 7)
