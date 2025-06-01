from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CePereiroSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2310803"
    name = "ce_pereiro"
    allowed_domains = ["pereiro.ce.gov.br"]
    BASE_URL = "https://www.pereiro.ce.gov.br"
    start_date = date(2020, 1, 3)
