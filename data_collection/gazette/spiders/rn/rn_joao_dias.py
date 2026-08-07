from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnJoaoDiasSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2405900"
    name = "rn_joao_dias"
    allowed_domains = ["joaodias.rn.gov.br"]
    BASE_URL = "https://www.joaodias.rn.gov.br"
    start_date = date(2022, 3, 21)
