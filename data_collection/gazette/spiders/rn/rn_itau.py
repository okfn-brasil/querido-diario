from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnItauSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2404903"
    name = "rn_itau"
    allowed_domains = ["itau.rn.gov.br"]
    BASE_URL = "https://www.itau.rn.gov.br"
    start_date = date(2021, 1, 4)
