from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CeTauaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2313302"
    name = "ce_taua"
    allowed_domains = ["taua.ce.gov.br"]
    BASE_URL = "https://www.taua.ce.gov.br"
    start_date = date(2019, 8, 30)
